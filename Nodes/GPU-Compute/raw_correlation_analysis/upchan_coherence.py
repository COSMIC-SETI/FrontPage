"""
Written by Savin Shynu Varghese:
    
A script to load dual antenna data from a single guppi raw file,
upchannelize the data from each antenna, conducts autocorrelation,
cross correlation and make diagnostic plots.

Currently set up to take one raw file. Uses blimpy for reading raw files and 
numpy for FFT (which is slower). Takes 3 minutes on average to do the FFT for a single file
data
"""

import sys,os
import time
from blimpy import GuppiRaw
import numpy as np
import matplotlib
import tqdm as tq
from matplotlib import pyplot as plt
import argparse
from sliding_rfi_flagger import flag_rfi

# matplotlib.use('Tkagg')

def main(args):
    tbeg = time.time()

    # Collecting the data from the guppi raw files and
    # saving them to an array

    filename = args.dat_file #Input guppi raw file 

    gob = GuppiRaw(filename) #Instantiating a guppi object

    header = gob.read_first_header() # Reading the first header 
    n_blocks = gob.n_blocks    # Number of blocks in the raw file
    nant_chans = int(header['OBSNCHAN'])
    nant = int(header['NANTS'])
    nbits = int(header['NBITS'])
    npols = int(header['NPOL'])
    nchan = int(nant_chans/nant)
    freq_mid = header['OBSFREQ'] #stopping frequency 
    del_t = header['TBIN']
    del_f = header['CHAN_BW']
    freq_start = freq_mid - ((nchan*del_f)/2.0)
    freq_end = freq_mid + ((nchan*del_f)/2.0)
    blocksize = header['BLOCSIZE']
    ntsamp_block = int(blocksize/(nant_chans*npols*2*(nbits/8))) # Number of time samples in the block
    ants = header['ANTNMS00']
    ants = ants.split(',')
    ntsamp_tot = args.tint/del_t #Total number of coarse time samples in the integration time.
    n_blocks_read = int(ntsamp_tot/ntsamp_block) # Number of blocks to read
    
    if  n_blocks_read > n_blocks:
        print(f"Warning: Given intg_time > duration of the file: {round(n_blocks*ntsamp_block*del_t)} s, Using maximum time duration of the file")
        n_blocks_read = n_blocks

    band_percentage = float(args.band)
    bandcenter_percentage = float(args.band_center)
    assert band_percentage > 0.0 and band_percentage <= 1.0

    band_bottom = bandcenter_percentage - (0.5 * band_percentage) # center case, default
    band_top = bandcenter_percentage + (0.5 * band_percentage) # center case, default
    assert band_bottom > 0.0 and band_bottom <= 1.0
    assert band_top > 0.0 and band_top <= 1.0

    print("The header info for the file: ")
    print(header)
    print(f"Nblocks: {n_blocks},  Number of blocks to read: {n_blocks_read}")
   

    # Collecting data from each block into a big array
    data = np.zeros((nant, nchan, int(ntsamp_block*n_blocks_read), npols), dtype = 'complex64')
    print("Started collecting data")
    for i in tq.tqdm(range(n_blocks_read)):
        head_block, data_block = gob.read_next_data_block()
        data[:,:, i*ntsamp_block:(i+1)*ntsamp_block, :] = data_block.reshape(nant, nchan, ntsamp_block, npols)

    # Upchannelize the data
    print("Starting upchannelization part")

    nfine = args.lfft # Number of fine channels per coarse channel
    nchan_fine = nchan*nfine
    
    # trim time to be a multiple of FFT size
    ntime_total = data.shape[2]
    ntime_total -= ntime_total % args.lfft
    data = data[:, :, 0:ntime_total, :]

    freq_range = freq_end - freq_start
    freq_end = freq_start + freq_range*band_top
    freq_start = freq_start + freq_range*band_bottom

    # Time, frequency resolution and number of time samples after FFT
    del_t = del_t*nfine
    ntsampfine = int(data.shape[2]/nfine)
    del_f = del_f/nfine


    # Reshaping the data for FFT
    print(f"Reshaping the data for FFT from {data.shape}")
    # reshape to [A,C,Tfine,Tfft,P]
    data = data.reshape(nant, nchan, ntsampfine, nfine, npols)
    
    ## trim channel to minimum:
    # transpose to [A,Tfine,C,Tfft,P]
    data = np.transpose(data, axes=(0,2,1,3,4))
    # reshape to [A,Tfine,C*Tfft,P]
    data = data.reshape(nant, ntsampfine, nchan_fine, npols)
    # select band
    band_lower = int(nchan_fine*band_bottom)
    band_upper = int(nchan_fine*band_top + 0.5)
    band_length = band_upper-band_lower
    ncoarse_chan_required = int(np.ceil(band_length/nfine))
    band_upper_padding = ncoarse_chan_required*nfine - band_length
    print(f"Selecting [{band_bottom}, {band_top}] of the channels data, range [{band_lower}, {band_upper}).")
    data = data[:, :, band_lower:band_upper+band_upper_padding, :]
    # reshape to [A, Tfine, C, Tfft, P]
    data = data.reshape(nant, ntsampfine, ncoarse_chan_required, nfine, npols)

    print(f"FFT of the data ({data.shape} along axis 3)")
    t0 = time.time()
    data = np.fft.fft(data, axis = 3)
    data = np.fft.fftshift(data, axes = 3)
    t1 = time.time()
    print(f"FFT done, took {t1-t0} s")

    print(f"The channelized datashape [A, Tfine, C, Cfine, P]: {data.shape}")
    data = data.reshape(nant, ntsampfine, ncoarse_chan_required*nfine, npols)
    if band_upper_padding > 0:
        data = data[:, :, 0:-band_upper_padding, :] # discard extra data
    print(f"The channelized datashape collapsed and filtered [A, Tfine, Cfine, P]: {data.shape}")
    

    print(f"The used datashape: {data.shape}")
    nchan = data.shape[2]
    freq_axis = np.linspace(freq_start, freq_end, nchan) #New Upchannelized frequency channels

    source_file_name = os.path.basename(args.dat_file)

    autocorr_mean_dict = {
        ants[ant1]: np.mean(data[ant1,...]*np.conjugate(data[ant1,...]), axis = 0, keepdims=False)
        for ant1 in range(0, nant)
    }
    plot_autocorrelations(
        autocorr_mean_dict, # {ant_name: [Chan, Pol]}
        freq_axis,
        source_file_name = source_file_name,
        plot_not_savefig = args.plot,
    )

    #Seperating out the data from two antennas into a different array and changing their order
    for ant1 in range(0, nant):
        for ant2 in range(ant1+1, nant):
            analyse(
                autocorr_mean_dict[ants[ant1]],
                autocorr_mean_dict[ants[ant2]],
                data[ant1,...]*np.conjugate(data[ant2,...]), # cross_corr
                [ants[ant1], ants[ant2]],
                del_t,
                del_f,
                freq_axis,
                source_file_name = source_file_name,
                plot_not_savefig = args.plot,
                measure_time_delay = args.time_delay,
                interactively_assess_channel = args.track
            )
    
    tend = time.time()
    print(f"Total processing time: {(tend-tbeg)/60.0} min")

    if args.plot:
        return
    plot_file_collection_id = f"{source_file_name}_{freq_axis[0]:0.3f}-{freq_axis[-1]:0.3f}"
    print(f"Plotted files for collection: *{plot_file_collection_id}*")
    return plot_file_collection_id

def plot_autocorrelations(
    autocorr_mean_dict, # {ant_name: [Chan, Pol]}
    freq_axis,
    source_file_name = "Unknown",
    plot_not_savefig = False,
    omit_phase = True,
    ncol = 4
):
    nant = len(autocorr_mean_dict)
    nrow = int(np.ceil(nant/ncol))
    fig, axs = plt.subplots(
        nrow,
        ncol,
        constrained_layout=True,
        figsize = (3*ncol,4*nrow),
        sharex=True
    )

    row_index = 0
    col_index = 0
    for ant_name, autocorr_mean in autocorr_mean_dict.items():

        axs[row_index,col_index].plot(freq_axis, 10*np.log10(np.abs(autocorr_mean[:,0])), label = 'pol 0')
        axs[row_index,col_index].plot(freq_axis, 10*np.log10(np.abs(autocorr_mean[:,1])), label = 'pol 1')
        axs[row_index,col_index].set_ylabel("Amplitude log scale (a.u.)")
        axs[row_index,col_index].set_xlabel("Frequency (MHz)")
        axs[row_index,col_index].set_title(f"Amplitude : {ant_name}")
        axs[row_index,col_index].legend()

        if not omit_phase:
            col_index += 1
            if col_index == ncol:
                col_index = 0
                row_index += 1
            axs[row_index,col_index+1].plot(freq_axis, np.angle(autocorr_mean[:,0], deg = True),  '.', label = 'pol 0')
            axs[row_index,col_index+1].plot(freq_axis, np.angle(autocorr_mean[:,1], deg = True), '.', label = 'pol 1')
            axs[row_index,col_index+1].set_ylabel("Phase (degrees)")
            axs[row_index,col_index+1].set_xlabel("Frequency (MHz)")
            axs[row_index,col_index+1].set_title(f"Phase: {ant_name}")
            axs[row_index,col_index+1].legend()

        col_index += 1
        if col_index == ncol:
            col_index = 0
            row_index += 1

    fig.suptitle(f"Autocorrelations: {source_file_name}")

    if plot_not_savefig:
        plt.show()
    else:
        filename = f"auto_corr_{source_file_name}_{freq_axis[0]:0.3f}-{freq_axis[-1]:0.3f}.png"
        plt.savefig(filename, dpi = 150)
        plt.close()

def analyse(
    autocorr_mean1, # [Chan, Pol]
    autocorr_mean2, # [Chan, Pol]
    cross_corr, # [Time, Chan, Pol]
    baseline_antnames,
    del_t,
    del_f,
    freq_axis,
    source_file_name = "Unknown",
    plot_not_savefig = False,
    measure_time_delay = False,
    interactively_assess_channel = False,
):
    nchan = autocorr_mean1.shape[0]
    mean_crosscorr_spec = np.mean(cross_corr, axis = 0, keepdims=False) # Cross correlations

    # Plotting the phase and amplitude of the autocorrelation for 2 antennas

    baseline_str = f"{baseline_antnames[0]}-{baseline_antnames[1]}"
    freqrange_str = f"{freq_axis[0]:0.3f}-{freq_axis[1]:0.3f}"

    sqrt_autos_pol0 = np.sqrt(autocorr_mean1[:,0]*autocorr_mean2[:,0])
    sqrt_autos_pol1 = np.sqrt(autocorr_mean1[:,1]*autocorr_mean2[:,1])
    mean_crosscorr_pol0_coeff = mean_crosscorr_spec[:,0]/sqrt_autos_pol0
    mean_crosscorr_pol1_coeff = mean_crosscorr_spec[:,1]/sqrt_autos_pol1

    #Plotting the phase and amplitude of the cross correlation

    fig, axs = plt.subplots(2, 2, constrained_layout=True, figsize = (10,8))

    axs[0,0].plot(freq_axis, np.angle(mean_crosscorr_spec[:,0], deg = True),  '.', label = 'pol 0')
    axs[0,0].set_ylabel("Phase (degrees)")
    axs[0,0].set_xlabel("Frequency (MHz)")
    axs[0,0].set_title(f"Crosscorrelation : {baseline_str}")
    axs[0,0].legend()

    axs[0,1].plot(freq_axis, np.angle(mean_crosscorr_spec[:,1], deg = True), '.', label = 'pol 1')
    axs[0,1].set_ylabel("Phase (degrees)")
    axs[0,1].set_xlabel("Frequency (MHz)")
    axs[0,1].set_title(f"Crosscorrelation : {baseline_str}")
    axs[0,1].legend()

    axs[1,0].plot(freq_axis, 10*np.log10(np.abs(mean_crosscorr_pol0_coeff)), label = 'pol 0')
    axs[1,0].set_ylabel("Amplitude (dB)")
    axs[1,0].set_xlabel("Frequency (MHz)")
    axs[1,0].set_title(f"Crosscorrelation Coefficient: {baseline_str}")
    axs[1,0].legend()

    axs[1,1].plot(freq_axis, 10*np.log10(np.abs(mean_crosscorr_pol1_coeff)), label = 'pol 1')
    axs[1,1].set_ylabel("Amplitude (dB)")
    axs[1,1].set_xlabel("Frequency (MHz)")
    axs[1,1].set_title(f"Crosscorrelation Coefficient: {baseline_str}")
    axs[1,1].legend()
    
    fig.suptitle(f"File: {source_file_name}")

    if  plot_not_savefig:
        plt.show()
    else:
        filename = f"cross_corr_{source_file_name}_{freqrange_str}_{baseline_str}.png"
        plt.savefig(filename, dpi = 150)
        plt.close()


    #Conduct an ifft of the crosscorrelated spectra to get the time delay plots
    if measure_time_delay:        
        #Conducting a step of RFI removal using sliding median window before doing ifft
        # Threshold for RFI removal
        threshold = 3
        
        #Getting bad channels
        bad_chan0 = flag_rfi(np.abs(mean_crosscorr_spec[:,0]), int(nchan/6), threshold)
        bad_chan1 = flag_rfi(np.abs(mean_crosscorr_spec[:,1]), int(nchan/6), threshold)
        
        # print(bad_chan0.shape[0], bad_chan1.shape[0])
        
        ##Zeroing bad channels
        mean_crosscorr_spec[bad_chan0[:,0],0] = 0
        mean_crosscorr_spec[bad_chan1[:,0],1] = 0

        #FFT of the spectra
        mean_crosscorr_pol0_ifft = np.fft.ifft(mean_crosscorr_spec[:,0])
        mean_crosscorr_pol1_ifft = np.fft.ifft(mean_crosscorr_spec[:,1]) 
        
        #FFT shift of the data
        mean_crosscorr_pol0_ifft = np.fft.ifftshift(mean_crosscorr_pol0_ifft)
        mean_crosscorr_pol1_ifft = np.fft.ifftshift(mean_crosscorr_pol1_ifft)

        #Defining  total frequency channels and fine channel bandwidths in Hz to get the time lags
        tlags = np.fft.fftfreq(nchan,del_f*1e+6)
        tlags = np.fft.fftshift(tlags)*1e+9 #Converting the time lag into us
        tmax_pol0 = np.argmax(10*np.log(np.abs(mean_crosscorr_pol0_ifft)))
        tmax_pol1 = np.argmax(10*np.log(np.abs(mean_crosscorr_pol1_ifft)))

        fig, (ax0, ax1) = plt.subplots(1, 2, constrained_layout=True, figsize = (10,8))

        ax0.plot(tlags, 10*np.log(np.abs(mean_crosscorr_pol0_ifft)), label = 'pol 0')
        ax0.set_ylabel("Power (a.u) log scale")
        ax0.set_xlabel(f"Time lags (delta t = {tlags[1] -tlags[0]}) ns)")
        ax0.set_title(f"{baseline_str}: time delay = {tlags[tmax_pol0]} ns")
        ax0.legend()

        ax1.plot(tlags, 10*np.log(np.abs(mean_crosscorr_pol1_ifft)), label = 'pol 1')
        ax1.set_ylabel("Power (a.u) log scale")
        ax1.set_xlabel(f"Time lags (delta t = {tlags[1] -tlags[0]} ns)")
        ax1.set_title(f"{baseline_str}: time delay = {tlags[tmax_pol1]} ns")
        ax1.legend()

        fig.suptitle(f"File: {source_file_name}")

        if plot_not_savefig:
            plt.show()
        else:
            filename = f"time_delay_{source_file_name}_{freqrange_str}_{baseline_str}.png"
            plt.savefig(filename, dpi = 150)
            plt.close()


    #Proceed if needed to track a channel as a function of time
    if interactively_assess_channel:
        #Tracking a channel as a function of time
        chan = int(input(f"Enter the channel (enumeration) to track [0={freq_axis[0]}, {nchan}={freq_axis[1]}]:"))
        #chan = np.where((abs(freq-chan) < 0.002))[0]
        #if len(chan) == 0:
        #   sys.exit("No such channel exist, cannot track")
        #print(chan)
    
        fig, (ax0, ax1) = plt.subplots(1, 2, constrained_layout=True, figsize = (10,8))
        
        ax0.plot(np.angle(cross_corr[:,chan,0] ,deg = True), '.', label = 'pol 0')
        ax0.set_ylabel("Phase (degrees)")
        ax0.set_xlabel(f"Time samples (delta t = {del_t} s)")
        ax0.set_title(f"Crosscorrelation : {baseline_str}")
        ax0.legend()

        ax1.plot(np.angle(cross_corr[:,chan,1] ,deg = True), '.', label = 'pol 1')
        ax1.set_ylabel("Phase (degrees)")
        ax1.set_xlabel(f"Time samples (delta t = {del_t} s)")
        ax1.set_title(f"Crosscorrelation : {baseline_str}")
        ax1.legend()
       
        fig.suptitle(f"File: {source_file_name}")

        if plot_not_savefig:
            plt.show()
        else:
            plt.savefig(f"chan_trac_{source_file_name}_{baseline_str}.png", dpi = 150)
            plt.close()


if __name__ == '__main__':
    
    # Argument parser taking various arguments
    parser = argparse.ArgumentParser(
        description='Reads guppi rawfiles, upchannelize, conducts auto and crosscorrelation',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d','--dat_file', type = str, required = True, help = 'GUPPI raw file to read in')
    parser.add_argument('-b','--band', type = float, required = False, default = 1.0,  help = 'Bandwidth to plot specified as a decimal percentage [0.0, 1.0], default:1.0')
    parser.add_argument('-bc','--band-center', type = float, required = False, default = 1.0,  help = 'Bandwidth center to plot specified as a decimal percentage [0.0, 1.0]-`band`, default:0.5')
    parser.add_argument('-f','--lfft', type = int, required = True, default = 120,  help = 'Length of FFT, default:120')
    parser.add_argument('-i', '--tint', type = float, required = True, help = 'Time to integrate in (s), default: whole file duration')
    parser.add_argument('-td', '--time_delay', action = 'store_true', help = 'If there are fringes, plot/save the time delay plot. An RFI filtering is conductted before the IFFT')
    parser.add_argument('-p', '--plot', action = 'store_true', help = 'plot the figures, otherwise save figures to working directory')
    parser.add_argument('-t', '--track', action = 'store_true', help = 'Track a channel as a function of time, need to enter a RFI free channel after inspection')

    args = parser.parse_args()


    main(args)

