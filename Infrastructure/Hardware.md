# COSMIC Hardware

## Hardware Specifications

### DTS Optical Hardware

- 5 x Fiberstore M6500-CH2U 7-slot 2U EDFA Chassus 
- 35 x Fiberstore M6200-25PA 25dB Gain DWDM EDFA
- 35 x Fiberstore M6200-SFPVOA Variable Optical Attenuator
- 28 x 12-channel DWDM demultiplexer

### FPGA Servers

- 3 x Tyan B7119F77V10E4HR-2T55-N 4U server

Each server comprises:

- 2 x Intel Xeon Silver 4208 CPU
- 6 x 16GB DDR4 Memory
- 5 x Alpha Data ADM-PCIE-9H7 FPGA card
- 10 x Alpha Data AD-PCIE-FQSFP quad-port QSFP28 adapter

### 100G Switches

- 2 x Cisco N9K-C9364C 64-port 100GbE Switch

### CPU/GPU Compute

- 16 x Supermicro 4124GS-TNR 4U GPU server

Each server comprises:

- 2 x AMD Epyc 7313/7413 CPU (first 16 servers have 7313)
- 16 x 32GB DDR Memory
- 2 x Mellanox MCX623106AS-CDAT dual port 100GbE
- 2 x Highpoint SSD7540 NVMe RAID
- 16 x 1TB Samsung 980 Pro NVMe
- 6 x PNY RTX A4000 GPU

### Storage

- 2 x Supermicro 6049P-E1CR36L 4U Storage Server

Each server comprises:

- 2 x Intel Xeon Silver 4210R CPU
- 8 x 32GB DDR4 Memory
- 36 x 16TB Seagate Exos X18 Enterprise HDD
- 1 x Mellanox MCX516A-CDAT dual-port 100GbE NIC
- Broadcom MegaRAID 9560-8i RAID card (inc. battery backup)

## Rack Layout

| SETI Rack #1       | SETI Rack #2          | SETI Rack #3 | SETI Rack #4 | SETI Rack #5  | SETI Rack #6  | SETI Rack #7  | U  |
|:------------------:|:---------------------:|:------------:|:------------:|:-------------:|:-------------:|:-------------:|:--:|
| Fiber Patch Panel  |                       |              |              |               |               |               | 42 |
| ^^^^^^^^^^^^^^^^^  |                       |              |              |               |               |               | 41 |
| cable management   |                       |              |              |               |               |               | 40 |
| cosmic-head        |                       |              |              |               |               |               | 39 |
| 100G-SW-1          |                       |              |              |               |               |               | 38 |
| ^^^^^^^^^          |                       |              |              |               |               |               | 37 |
| switch mount shelf |                       |              |              |               |               |               | 36 |
| 100G-SW-0          |                       |              |              |               |               |               | 35 |
| ^^^^^^^^^          |                       |              |              |               |               |               | 34 |
| cable management   |                       |              |              |               |               |               | 33 |
| demux ant 29-30    |                       |              |              |               |               |               | 32 |
| demux              |                       |              |              |               |               |               | 31 |
| demux              |                       |              |              |               |               |               | 30 |
| demux              |                       |              |              |               |               |               | 29 |
| demux              |                       |              |              |               |               |               | 28 |
| cable management   |                       |              |              |               |               |               | 27 |
| demux              | cosmic-storage-2      |              |              |               |               |               | 26 |
| demux              |                       |              |              |               |               |               | 25 |
| demux              |                       |              |              |               |               |               | 24 |
| demux              |                       |              |              |               |               |               | 23 |
| demux              | cosmic-storage-1      |              |              |               |               |               | 22 |
| cable management   |                       |              |              |               |               |               | 21 |
| demux              |                       |              |              |               |               |               | 20 |
| demux              |                       |              |              |               |               |               | 19 |
| demux              |                       |              |              |               |               |               | 18 |
| demux              |                       |              |              |               |               |               | 17 |
| demux ant 1-2      |                       | cosmic-gpu-5 | cosmic-gpu-9 | cosmic-gpu-13 | cosmic-gpu-17 |               | 16 |
| cable management   |                       |              |              |               |               |               | 15 |
| cosmic-fpga-2      |                       |              |              |               |               |               | 14 |
| ^^^^^^^^^^^^^      |                       |              |              |               |               |               | 13 |
| ^^^^^^^^^^^^^      |                       | cosmic-gpu-4 | cosmic-gpu-8 | cosmic-gpu-12 | cosmic-gpu-16 | cosmic-gpu-20 | 12 |
| ^^^^^^^^^^^^^      | cosmic-gpu-1          |              |              |               |               |               | 11 |
| blank panel        |                       |              |              |               |               |               | 10 |
| cosmic-fpga-1      |                       |              |              |               |               |               | 9  |
| ^^^^^^^^^^^^^      | unused supermicro box | cosmic-gpu-3 | cosmic-gpu-7 | cosmic-gpu-11 | cosmic-gpu-15 | cosmic-gpu-19 | 8  |
| ^^^^^^^^^^^^^      |                       |              |              |               |               |               | 7  |
| ^^^^^^^^^^^^^      |                       |              |              |               |               |               | 6  |
| blank panel        |                       |              |              |               |               |               | 5  |
| cosmic-fpga-0      | cosmic-gpu-0          | cosmic-gpu-2 | cosmic-gpu-6 | cosmic-gpu-10 | cosmic-gpu-14 | cosmic-gpu-18 | 4  |
| ^^^^^^^^^^^^^      |                       |              |              |               |               |               | 3  |
| ^^^^^^^^^^^^^      |                       |              |              |               |               |               | 2  |
| ^^^^^^^^^^^^^      |                       |              |              |               |               |               | 1  |
