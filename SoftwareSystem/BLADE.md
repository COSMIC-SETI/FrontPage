# Overview

Beam-formation at the VLA is accomplished with the [BLADE](https://github.com/MydonSolutions/blade/tree/0.7-cli-seticore) command-line program.

BLADE is primarily a framework for DSP pipelines. The kernels used for each module of the arverarching pipeline can have different implementations: one "phasor" kernel may require delays as an input while another might internally calculate these from antenna positions and beamforming coordinates. 
BLADE's exposed pipelines are static arrangments of its modules to achieve certain ends. The pipelines are referred to via a telescope-mode pair. BLADE's beamforming pipeline that the VLA uses is mode BS of telescope ATA. Mode BS refers to Beamform-Search, while the telescope is ATA as the phasor module was developed for the ATA.

# Beamformation Pipeline

## Inputs

### CLI Arguments

A specification of upchannelisation rate (`F`), coarse channel ingest rate (`C`) and fine-spectra beamform-search rate (`T`) determines the data shape that flows through the pipeline:

- Ingest `F` coarse-spectra of `C` channels
- Upchannelise `F` coarse-spectra, accumulating `T` fine-spectra
- Beamform `T` fine-spectra
- Search `T` fine-spectra

### BFR5 File

Of the [BFR5 file's contents](https://docs.google.com/document/d/1H-FYir9tiCYYJGGW8EDApfcQRyrN-ptUczheaJp2ZF8/edit?usp=sharing), BLADE 's ATA mode B only accesses a portion. As the phasors are internally calculated, the delays field is ignored. The frequency-array is also ignored as the frequency of each channel is inferred from the key-values of the first RAW header. 

Dataset | Units | Notes
-|-|-
/diminfo/nants | | Validated against RAW block dimensions.
/diminfo/npol | | Validated against RAW block dimensions.
/diminfo/nchan | | Validated against RAW block dimensions.
/diminfo/nbeams | | Validated against RAW block dimensions.
/diminfo/ntimes | | Validated against RAW block dimensions.
/telinfo/latitude | degrees | Provides reference position to translate to ECEF coordinates if necessary.
/telinfo/longitude | degrees | Provides reference position to translate to ECEF coordinates if necessary.
/telinfo/altitude | metres | Provides reference position to translate to ECEF coordinates if necessary.
/telinfo/antenna_positions | metres | These must be in the order of the RAW antenna data as no re-ordering is currently applied.
/telinfo/antenna_position_frame | {'ecef', 'enu', 'xyz'} | 'xyz' value indicates that the positions are relative to the LLA. If not 'ecef', provided positions are converted to the ECEF frame.
/obsinfo/phase_center_ra | radians | Provides phase-center coordinate.
/obsinfo/phase_center_dec | radians | Provides phase-center coordinate.
/calinfo/cal_all | | Provides calibration coeffecients wich are applied as factors to the phasor-cooffecients calculated to perform the beamforming.
/beaminfo/src_names | | Names for each beam to be formed.
/beaminfo/ras | radians | Coordinates for each beam to be formed.
/beaminfo/decs | radians | Coordinates for each beam to be formed.

### GUPPI RAW File

Further information is attained from the first RAW header:

Data | Header key(s) | Notes
-|-|-
Delta against UT1 | DUT1 |
Channel Bandwidth | CHAN_BW | This is the bandwidth of the recorded channels.
F-Engine Number of Channels | FECHAN | This is the number of channels in the observation (not in the recording).
Recording Starting Channel | SCHAN | This is the sub-band offset for the recording within the observation.
Observation center frequency | `OBSFREQ + (- NCHAN/2 - SCHAN + FENCHAN/2)*CHAN_BW` | This is the center of the observation's frequency (L.O. frequency), not that of the recording. It is used by the phasor module to determine the fringe frequency (first channel frequency of the observation). OBSFREQ is also to be the center-frequency of the middle most recorded channel. 
Start Unix Epoch-Seconds | `SYNCTIME + ((NTIME * 1.0/CHAN_BW) / PIPERBLK) * PKTIDX` | This is the starting julian-date of the recording. The phasor uses the middle of each RAW block in the calculation of the delays.

## Pre-beamformer Upchannelisation

The upchannelisation produces 1 fine-spectrum at a time as that is when the kernel is most efficient. The fine-spectra are accumulated into a batch before passing downstream. With each fine-spectral output come the following bits of metadata:

Fine-spectra Metadata | Notes
-|-
Time (MJD) | This timestamps the middle of the spectra-batch.
DUT1 (seconds) | This comes from the first header of the RAW input.
Coarse-channel offset | This requirement is a consequence of processing subbands of coarse-channels at a time.

## Beamformation Calculation

The ATA phasor module internally calculates delays for the antenna from their positions relative to the coordinates of the beams being formed.
The delays are calculated from a UVW transformation achieved by using ERFA's `eraApco13`, `eraAtciq` and `eraAtioq` methods (effecting the `eraAtco13` method) to produce hour angle and declination values for each beam. They are also made relative to phase-center and to the reference antenna. The required values are as follows:

Value (Units) | Source (Units)
-|-
LLA (radians, radians, metres) | BFR5 (radians, radians, metres)
Antenna Positions (LLA-relative metres) | BFR5 (ECEF (standardised ingest))
Time (Modified JD) | Fine-spectra Metadata (Modified JD)
DUT1 (seconds) | Fine-spectra Metadata (seconds)
Phase-center (radians, radians) | BFR5 (radians, radians)
Beam Coordinates (radians, radians) | BFR5 (radians, radians)
Reference Antenna Index | 0

Thereafter the beams' phasors are calculated for each antenna-channel based on the channel's middle-frequency and the antenna-beam delay:

```
fringeRateExp = -j * 2 * PI * delay * (bottomFrequencyHz + coarseChannelOffset * coarseChannelBandwidthHz) 
for f in 0:numberOfFineFrequencyChannels-1:
  channelMidFreq = (f + 0.5) * coarseChannelBandwidthHz / upchannelisationRate
  phasorsExp = -j * 2 * PI * delay * channelMidFreq
  phasor = e^(phasorsExp + fringeRateExp)
```

The phasors are further mutliplied by the antenna-calibration coefficients (sourced from the BFR5). The calibration coefficients are repeated for all the fine-channels of a coarse channel, as it is expected that the calibration-coefficients are specified for coarse-channels.

## Dedoppler Search

The signal search kernel is provided by [seticore](https://github.com/lacker/seticore). While BLADE's ATA mode B only forms beams and output filterbank files, ATA mode BS forms beams and uses seticore to search for signals within those beams. The output is a `signals` and `hits` file pair:

- `.hits` files hold [data](https://github.com/lacker/seticore/blob/master/hit.capnp) describing the various signals found by the search kernel.
- `.stamps` files hold multiple stamps of the RAW data that lead to detected signals. The stamp is of upchannelized RAW data (prior to beamformation). Multiple hits may have their source in the same or very close region of the RAW data, so stamps are made of regions ascertained after grouping hits within a given margin.

# Operation

## Idiosyncrasies

As the pipeline begins with upchannelisation which produces a single fine-spectrum at a time, small upchannelisation rates infer many copies of relatively small amounts of data, leading to inefficiencies.
Furthermore, Direct-IO opened RAW files must be read in whole multiples of 512 bytes. This imposes a lower limit on the upchannelisation rate relative to the sample byte-size of the file: `upchannelisation_rate_lower_limit = 512 / (num_pol * 2 * num_bits)`. For an 8-bit RAW file (2 bytes per complex sample), the lower limit of upchannelisation is 128.