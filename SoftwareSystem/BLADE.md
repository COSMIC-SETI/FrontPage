# Overview

Beam-formation at the VLA is accomplished with the [BLADE](https://github.com/MydonSolutions/blade/tree/0.7-cli-seticore) command-line program.

BLADE is primarily a framework for DSP pipelines. The kernels used for each module of the arverarching pipeline can have different implementations: one "phasor" kernel may require delays as an input while another might internally calculate these from antenna positions and beamforming coordinates. 
BLADE's exposed pipelines are static arrangments of its modules to achieve certain ends. The pipelines are referred to via a telescope-mode pair. BLADE's beamforming pipeline that the VLA uses is mode BS of telescope ATA. Mode BS refers to Beamform-Search, while the telescope is ATA as the phasor module was developed for the ATA.

# Beamformation Pipeline

![BLADE ATA CLI Pipeline](./img/BLADE.png)

## Inputs

### CLI Arguments

Issuing `blade-cli -t ATA --help` will produce explicit usage information and should be the prioritised source for this information.

A specification of upchannelisation rate (`Tu`), coarse channel ingest rate (`Fc`) and fine-spectra beamform-search rate (`T`) determines the data shape that flows through the pipeline:

- Ingest `Tu` coarse-spectra of `Fc` channels
- Upchannelise `Tu` coarse-spectra, gathering `T` fine-spectra
- Beamform `T` fine-spectra (using the time-stamp of the first spectrum to calculate phasors)
- Search `T` fine-spectra

Further arguments are exposed to control the dedoppler search:

- SNR threshold
- Drift-rate minimum
- Drift-rate maximum
- Exclude hits with drift rate of zero

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

Note that the beamformation computes phasors once per input as each input is accompanied by a scalar time-stamp. When the beamformer gathers spectra it averages the time-stampes of the spectra and use the average for the calculation of the phasors.

The ATA phasor module internally calculates delays for the antenna from their positions relative to the coordinates of the beams being formed.
The delays are calculated from a UVW transformation achieved by using ERFA's `eraApco13`, `eraAtciq` and `eraAtioq` methods (effecting the `eraAtco13` method) to produce hour angle and declination values for each beam. They are also made relative to phase-center and to the reference antenna. The required values are as follows:

Value (Units) | Source (Units) | Notes
-|-
LLA (radians, radians, metres) | BFR5 (radians, radians, metres) |
Antenna Positions (LLA-relative metres) | BFR5 (ECEF (standardised ingest)) |
Time (Modified JD) | Fine-spectra Metadata (Modified JD) | This is a scalar value for all the input spectra, the average time of each spectra.
DUT1 (seconds) | Fine-spectra Metadata (seconds) |
Phase-center (radians, radians) | BFR5 (radians, radians) |
Beam Coordinates (radians, radians) | BFR5 (radians, radians) |
Reference Antenna Index | 0 |

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

The Dedoppler search has an SNR threshold argument (exposed at the CLI), below which hits are dismissed. The full list of hits that are above the threshold populate the output `.hits` file, but because a Hit (capitilised to indicate it is qualitatively real) may be represented by many hits, a grouping process is undertaken to select a single representative hit.
The representative hit has the largest ['score'](https://github.com/MydonSolutions/seticore/blob/ce15906a10afe8705b5d9893d5a8affa1149b99d/dedoppler_hit.cpp#L40-49) of all the hits found within a ['margin'](https://github.com/MydonSolutions/seticore/blob/ce15906a10afe8705b5d9893d5a8affa1149b99d/dedoppler_hit_group.cpp#L36-64).
The representative hits are further screened against drift-rate rules (exposed at the CLI).
The `.stamps` file holds the stamps made from each group-representative hit that has relevant a drift-rate.

# Operation

## Idiosyncrasies

Direct-IO opened RAW files must be read in whole multiples of 512 bytes. This imposes a lower limit on the upchannelisation rate relative to the sample byte-size of the file: `upchannelisation_rate_lower_limit = 512 / (num_coarse_channel_ingest * num_pol * 2 * num_bits)`. For an 8-bit RAW file (2 bytes per complex sample), the lower limit of upchannelisation is 128, if the coarse-channel ingest rate is 1.

As the pipeline begins with upchannelisation which produces a single fine-spectrum at a time, small upchannelisation rates infer many copies of relatively small amounts of data, leading to inefficiencies. As can be inferred from the above, another factor of the ingest datasize, asides from the upchannelisation rate, is the coarse-channel ingest rate parameter. The coarse-channel ingest rate can be used to increase the data-rate and possibly mitigate some inefficiency when performing low upchannelisation operations.

## Optimsations

Optimal employment of BLADE hinges on understanding the underlying processes. Insider summative tips follow.

**GUPPI RAW Ingest**

The library used to ingest GUPPI RAW is [guppirawc99](https://github.com/MydonSolutions/guppirawc99). It enables iteration through the RAW data in arbitrary steps. As its [benchmarks show](https://github.com/MydonSolutions/guppirawc99#benchmarks), however, ingesting less than a RAW block's time-span of samples greatly reduces the achievable throughput.

The "upchannelisation rate" CLI argument directly determines how many timesamples are ingested at a time.

**BLADE's Beamformer**

The beamformer kernel for BLADE is optimised for data-shapes with greater number of spectra.

The "number of fine-spectra" CLI argument directly determines how many spectra the beamformer operates on at a time. But, as per the note in the [Beamformation Section](#beamformation-calculation), the phasors are calculated for one time-stamp across all the input spectra.

**seticore's Dedoppler Search**

For a worthwhile signal search to be conducted, at least 10 spectra should be provided.

The "number of fine-spectra" CLI argument directly determines how many spectra the seticore search operates on at a time.

