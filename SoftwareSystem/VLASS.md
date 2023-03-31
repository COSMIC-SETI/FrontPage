(cosmic_vla) cosmic@cosmic-gpu-0:/mnt/buf0/maser_w51_5991$ blade-cli -t ATA --help
BLADE [INFO]  | [CLI] 

Welcome to BLADE (Breakthrough Listen Accelerated DSP Engine)!
Version 0.7.4 | Build Type: release | Commit: 14372eea3
                   .-.
    .-""`""-.    |(0 0)
 _/`oOoOoOoOo`\_ \ \-/
'.-=-=-=-=-=-=-.' \/ \
  `-=.=-.-=.=-'    \ /\
     ^  ^  ^       _H_ \ art by jgs
    
BLADE (Breakthrough Listen Accelerated DSP Engine) - Command Line Tool - ATA
Usage: blade-cli [OPTIONS] input recipe output

Positionals:
  input TEXT REQUIRED         Input GUPPI RAW filepath
  recipe TEXT REQUIRED        Input BFR5 filepath
  output TEXT REQUIRED        Output filepath

Options:
  -h,--help                   Print this help message and exit
  -t,--telescope ENUM:value in {GENERIC->,ATA->} OR {,} REQUIRED
                              Telescope ID (ATA)
  -m,--mode ENUM:value in {B->,BS->,MODE_BS->,MODE_B->} OR {,,,} REQUIRED
                              Mode ID (MODE_B, MODE_BS)
  -i,--input TEXT REQUIRED    Input GUPPI RAW filepath
  -r,--recipe TEXT REQUIRED   Input BFR5 filepath
  -o,--output TEXT REQUIRED   Output filepath
  -N,--number-of-workers UINT [1] 
                              Number of workers
  -c,--pre-beamformer-channelizer-rate UINT [1024] 
                              Pre-beamformer channelizer rate (FFT-size)
  -T,--step-number-of-time-samples UINT [32] 
                              Step number of time samples
  -C,--step-number-of-frequency-channels UINT [32] 
                              Step number of frequency channels
  --input-type ENUM:value in {F64->,F16->,F32->,I8->,CF64->,CF32->,CF16->,CI8->} OR {,,,,,,,} REQUIRED
                              Input type format (CI8, CF16, CF32, I8, F16, F32)
  --output-type ENUM:value in {F64->,F16->,F32->,I8->,CF64->,CF32->,CF16->,CI8->} OR {,,,,,,,} REQUIRED
                              Output type format (CI8, CF16, CF32, I8, F16, F32)
  -s,--search-snr-threshold FLOAT [6] 
                              SETI search SNR threshold
  -d,--search-drift-rate-minimum FLOAT [0] 
                              SETI search drift rate minimum
  -D,--search-drift-rate-maximum FLOAT [50] 
                              SETI search drift rate maximum
  -Z,--search-drift-rate-exclude-zero
                              SETI search exclude hits with drift rate of zero
  -I,--incoherent-beam-enable Beamform the incoherent beam