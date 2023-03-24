The below is a walkthrough of how the BLADE ATA mode BS process currently executes.

Symbol | Value
-|-
`Fc` | Number of Coarse Frequency Channels
`Tu` | Number of Timesamples per Fine-spectrum (upchannelisation rate)
`F` | Number of Fine Frequency Channels (`Fc*Tu`)
`T` | Number of Fine-spectra
`Fs` | Number of Fine Frequency Channels to search
`A` | Number of Antenna
`B` | Number of Beams
`Bs` | Number of Beams to search
`P` | Number of Polarties
`S` | Number of bytes per complex sample

- A.1) Ingest `Fc` coarse-channels of enough timesamples (`Tu`) to produce 1 fine-spectrum.
  - Data is read from the disk into RAM
  - RAM usage: `A*Fc*Tu*P*S` bytes, VRAM usage: `0` Bytes
  - Dimensionality (Slowest->Fastest): A,F,T,P

- A.2) Channelize 1 fine-spectrum.
  - Data is transferred from RAM to VRAM
  - RAM usage: `0` bytes, VRAM usage: `A*F*1*P*S` Bytes
  - Dimensionality (Slowest->Fastest): A,F,T,P

- A.3) Collect `T` fine-spectra.
  - Data is collected in VRAM, being transferred within VRAM
  - RAM usage: `0` bytes, VRAM usage: `A*F*T*P*S` Bytes
  - Dimensionality (Slowest->Fastest): A,F,T,P

- A.4) Beamform `T` fine-spectra and detect producing {Beams=`B`, Freq=`Tu*Fc`, Time=`T`, Polarity=`1`}.
  - ***Use the time-stamp of the first fine-spectrum to calculate phasors with dimension of {Antenna=`A`, Freq=`Tu*Fc`, Time=1, Polarity=`P`}***
  - Data is transferred within VRAM
  - RAM usage: `0` bytes, VRAM usage: `B*F*T*P*S` Bytes
  - Dimensionality (Slowest->Fastest): B,T,P,F

- A.5) Search `T` fine-spectra producing `.hits` and `.stamps` files.
  - Data is transferred within VRAM
  - RAM usage: `0` bytes, VRAM usage: `B*F*T*P*S` Bytes

<details><summary>Ideally</summary>

- B.1) Ingest `Fc` coarse-channels of enough timesamples (`Tu`) to produce 1 fine-spectrum.
  - Data is read from the disk into RAM
  - RAM usage: `A*Fc*Tu*P*S` bytes, VRAM usage: `0` Bytes
  - Dimensionality (Slowest->Fastest): A,F,T,P

- B.2) Channelize 1 fine-spectrum.
  - Data is transferred from RAM to VRAM
  - RAM usage: `0` bytes, VRAM usage: `A*F*1*P*S` Bytes
  - Dimensionality (Slowest->Fastest): A,F,T,P

- B.3) Beamform `1` fine-spectra, and detect producing {Beams=`B`, Freq=`Tu*Fc`, Time=`1`, Polarity=`1`}.
  - ***Use the time-stamp of the fine-spectrum to calculate phasors with dimension of {Antenna=`A`, Freq=`Tu*Fc`, Time=1, Polarity=`P`}***
  - Data is transferred within VRAM
  - RAM usage: `0` bytes, VRAM usage: `B*F*1*P*S` Bytes
  - Dimensionality (Slowest->Fastest): B,T,P,F

- B.4) Collect `T` fine-spectra.
  - Data is collected in RAM, being transferred from VRAM to RAM
  - RAM usage: `B*F*T*P*S` bytes, VRAM usage: `0` Bytes
  - Dimensionality (Slowest->Fastest): B,T,P,F

- B.5) Search `Fs` fine-frequencies and `Bs` beams producing `.hits` and `.stamps` files, exhausting all collected data.
  - Data is transferred from RAM to VRAM
  - RAM usage: `0` bytes, VRAM usage: `Bs*Fs*T*P*S` Bytes
</details>