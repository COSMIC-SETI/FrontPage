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

- 22 x Supermicro 4124GS-TNR 4U GPU server (`cosmic-gpu2` - `cosmic-gpu-22`)

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

There are 10 COSMIC racks currently energized.
These are formed of a row of 7 racks, and a row of 3 racks.
Racks face each other, with a central "cold aisle".
Rack 8, 9, 10 are opposite racks 5, 6, 7, respectively, separated by 48 inches.

### Racks 1 - 7

_*Front-Mounted*_

| U  | SETI Rack #1          | SETI Rack #2       | SETI Rack #3   | SETI Rack #4   | SETI Rack #5    | SETI Rack #6    | SETI Rack #7    | U  |
|:--:|:---------------------:|:------------------:|:--------------:|:--------------:|:---------------:|:---------------:|:---------------:|:--:|
| 42 | Fiber Patch Panel     |                    |                |                |                 |                 |                 | 42 |
| 41 | `^^^^^^^^^^^^^^^^^`   |                    |                |                |                 |                 |                 | 41 |
| 40 | blank panel           |                    |                |                |                 |                 |                 | 40 |
| 39 | `cosmic-head`         |                    |                |                |                 |                 |                 | 39 |
| 38 | blank panel           |                    |                |                |                 |                 |                 | 38 |
| 37 | blank panel           |                    |                |                |                 |                 |                 | 37 |
| 36 | switch mount shelf    |                    |                |                |                 |                 |                 | 36 |
| 35 | blank panel           |                    |                |                |                 |                 |                 | 35 |
| 34 | blank panel           |                    |                |                |                 |                 |                 | 34 |
| 33 | blank panel           |                    |                |                |                 |                 |                 | 33 |
| 32 | blank panel           |                    |                |                |                 |                 |                 | 32 |
| 31 | blank panel           |                    |                |                |                 |                 |                 | 31 |
| 30 | blank panel           |                    |                |                |                 |                 |                 | 30 |
| 29 | blank panel           |                    |                |                |                 |                 |                 | 29 |
| 28 | blank panel           |                    |                |                |                 |                 |                 | 28 |
| 27 | blank panel           |                    |                |                |                 |                 |                 | 27 |
| 26 | blank panel           | `cosmic-storage-2` |                |                |                 |                 |                 | 26 |
| 25 | blank panel           | `^^^^^^^^^^^^^^^^` |                |                |                 |                 |                 | 25 |
| 24 | blank panel           | `^^^^^^^^^^^^^^^^` |                |                |                 |                 |                 | 24 |
| 23 | blank panel           | `^^^^^^^^^^^^^^^^` |                |                |                 |                 |                 | 23 |
| 22 | blank panel           | `cosmic-storage-1` |                |                |                 |                 |                 | 22 |
| 21 | blank panel           | `^^^^^^^^^^^^^^^^` |                |                |                 |                 |                 | 21 |
| 20 | blank panel           | `^^^^^^^^^^^^^^^^` |                |                |                 |                 |                 | 20 |
| 19 | blank panel           | `^^^^^^^^^^^^^^^^` |                |                |                 |                 |                 | 19 |
| 18 | blank panel           |                    |                |                |                 |                 |                 | 18 |
| 17 | blank panel           |                    |                |                |                 |                 |                 | 17 |
| 16 | blank panel           |                    | `cosmic-gpu-5` | `cosmic-gpu-9` | `cosmic-gpu-13` | `cosmic-gpu-17` |                 | 16 |
| 15 | blank panel           |                    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` |                 | 15 |
| 14 | `cosmic-fpga-2`       |                    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` |                 | 14 |
| 13 | `^^^^^^^^^^^^^`       |                    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` |                 | 13 |
| 12 | `^^^^^^^^^^^^^`       |                    | `cosmic-gpu-4` | `cosmic-gpu-8` | `cosmic-gpu-12` | `cosmic-gpu-16` | `cosmic-gpu-20` | 12 |
| 11 | `^^^^^^^^^^^^^`       | `cosmic-gpu-1`     | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 11 |
| 10 | blank panel           | `^^^^^^^^^^^^`     | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 10 |
| 9  | `cosmic-fpga-1`       |                    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 9  |
| 8  | `^^^^^^^^^^^^^`       | FPGA test server   | `cosmic-gpu-3` | `cosmic-gpu-7` | `cosmic-gpu-11` | `cosmic-gpu-15` | `cosmic-gpu-19` | 8  |
| 7  | `^^^^^^^^^^^^^`       |                    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 7  |
| 6  | `^^^^^^^^^^^^^`       |                    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 6  |
| 5  | blank panel           |                    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 5  |
| 4  | `cosmic-fpga-0`       | `cosmic-gpu-0`     | `cosmic-gpu-2` | `cosmic-gpu-6` | `cosmic-gpu-10` | `cosmic-gpu-14` | `cosmic-gpu-18` | 4  |
| 3  | `^^^^^^^^^^^^^`       | `^^^^^^^^^^^^^`    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 3  |
| 2  | `^^^^^^^^^^^^^`       | `^^^^^^^^^^^^^`    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 2  |
| 1  | `^^^^^^^^^^^^^`       | `^^^^^^^^^^^^^`    | `^^^^^^^^^^^^` | `^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | `^^^^^^^^^^^^^` | 1  |

_*Rear-Mounted*_

| U  | SETI Rack #1          | SETI Rack #2         | SETI Rack #3         | SETI Rack #4         | SETI Rack #5         | SETI Rack #6         |      SETI Rack #7    | U  |
|:--:|:---------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------:|:--------------------:|:--:|
| 42 | `cosmic-1g-switch-0`  | `cosmic-1g-switch-1` | `cosmic-1g-switch-2` | `cosmic-1g-switch-3` | `cosmic-1g-switch-4` | `cosmic-1g-switch-5` | `cosmic-1g-switch-6` | 42 |
| 41 | cable management      |                      |                      |                      |                      |                      |                      | 41 |
| 40 | blank panel           |                      |                      |                      |                      |                      |                      | 40 |
| 39 |                       |                      |                      |                      |                      |                      |                      | 39 |
| 38 | `cosmic-100g-switch-1`|                      |                      |                      |                      |                      |                      | 38 |
| 37 | `^^^^^^^^^^^^^^^^^^^^`|                      |                      |                      |                      |                      |                      | 37 |
| 36 | switch mount shelf    |                      |                      |                      |                      |                      |                      | 36 |
| 35 | `cosmic-100g-switch-0`|                      |                      |                      |                      |                      |                      | 35 |
| 34 | `^^^^^^^^^^^^^^^^^^^^`|                      |                      |                      |                      |                      |                      | 34 |
| 33 | cable management      |                      |                      |                      |                      |                      |                      | 33 |
| 32 | demux ant 29-30       |                      |                      |                      |                      |                      |                      | 32 |
| 31 | demux ant 27-28       |                      |                      |                      |                      |                      |                      | 31 |
| 30 | demux ant 25-26       |                      |                      |                      |                      |                      |                      | 30 |
| 29 | demux ant 23-24       |                      |                      |                      |                      |                      |                      | 29 |
| 28 | demux ant 21-22       |                      |                      |                      |                      |                      |                      | 28 |
| 27 | cable management      |                      |                      |                      |                      |                      |                      | 27 |
| 26 | demux ant 19-20       |                      |                      |                      |                      |                      |                      | 26 |
| 25 | demux ant 17-18       |                      |                      |                      |                      |                      |                      | 25 |
| 24 | demux ant 15-16       |                      |                      |                      |                      |                      |                      | 24 |
| 23 | demux ant 13-14       |                      |                      |                      |                      |                      |                      | 23 |
| 22 | demux ant 11-12       |                      |                      |                      |                      |                      |                      | 22 |
| 21 | cable management      |                      |                      |                      |                      |                      |                      | 21 |
| 20 | demux ant 9-10        |                      |                      |                      |                      |                      |                      | 20 |
| 19 | demux ant 7-8         |                      |                      |                      |                      |                      |                      | 19 |
| 18 | demux ant 5-6         |                      |                      |                      |                      |                      |                      | 18 |
| 17 | demux ant 3-4         |                      |                      |                      |                      |                      |                      | 17 |
| 16 | demux ant 1-2         |                      |                      |                      |                      |                      |                      | 16 |
| 15 | cable management      |                      |                      |                      |                      |                      |                      | 15 |
| 14 |                       |                      |                      |                      |                      |                      |                      | 14 |
| 13 |                       |                      |                      |                      |                      |                      |                      | 13 |
| 12 |                       |                      |                      |                      |                      |                      |                      | 12 |
| 11 |                       |                      |                      |                      |                      |                      |                      | 11 |
| 10 | cable management      |                      |                      |                      |                      |                      |                      | 10 |
| 9  |                       |                      |                      |                      |                      |                      |                      | 9  |
| 8  |                       |                      |                      |                      |                      |                      |                      | 8  |
| 7  |                       |                      |                      |                      |                      |                      |                      | 7  |
| 6  |                       |                      |                      |                      |                      |                      |                      | 6  |
| 5  | cable management      |                      |                      |                      |                      |                      |                      | 5  |
| 4  |                       |                      |                      |                      |                      |                      |                      | 4  |
| 3  |                       |                      |                      |                      |                      |                      |                      | 3  |
| 2  |                       |                      |                      |                      |                      |                      |                      | 2  |
| 1  |                       |                      |                      |                      |                      |                      |                      | 1  |

### Racks 8 - 10

_*Front-Mounted*_

| U  | SETI Rack #8    | SETI Rack #9    | SETI Rack #10   | U  |
|:--:|:---------------:|:---------------:|:---------------:|:--:|
| 42 |                 |                 |                 | 42 |
| 41 |                 |                 |                 | 41 |
| 40 |                 |                 |                 | 40 |
| 39 |                 |                 |                 | 39 |
| 38 |                 |                 |                 | 38 |
| 37 |                 |                 |                 | 37 |
| 36 |                 |                 |                 | 36 |
| 35 |                 |                 |                 | 35 |
| 34 |                 |                 |                 | 34 |
| 33 |                 |                 |                 | 33 |
| 32 |                 |                 |                 | 32 |
| 31 |                 |                 |                 | 31 |
| 30 |                 |                 |                 | 30 |
| 29 |                 |                 |                 | 29 |
| 28 |                 |                 |                 | 28 |
| 27 |                 |                 |                 | 27 |
| 26 |                 |                 |                 | 26 |
| 25 |                 |                 |                 | 25 |
| 24 |                 |                 |                 | 24 |
| 23 |                 |                 |                 | 23 |
| 22 |                 |                 |                 | 22 |
| 21 |                 |                 |                 | 21 |
| 20 |                 |                 |                 | 20 |
| 19 |                 |                 |                 | 19 |
| 18 |                 |                 |                 | 18 |
| 17 |                 |                 |                 | 17 |
| 16 |                 |                 |                 | 16 |
| 15 |                 |                 |                 | 15 |
| 14 |                 |                 |                 | 14 |
| 13 |                 |                 |                 | 13 |
| 12 | `cosmic-gpu-23` |                 |                 | 12 |
| 11 | `^^^^^^^^^^^^^` |                 |                 | 11 |
| 10 | `^^^^^^^^^^^^^` |                 |                 | 10 |
| 9  | `^^^^^^^^^^^^^` |                 |                 | 9  |
| 8  | `cosmic-gpu-22` |                 |                 | 8  |
| 7  | `^^^^^^^^^^^^^` |                 |                 | 7  |
| 6  | `^^^^^^^^^^^^^` |                 |                 | 6  |
| 5  | `^^^^^^^^^^^^^` |                 |                 | 5  |
| 4  | `cosmic-gpu-21` |                 |                 | 4  |
| 3  | `^^^^^^^^^^^^^` |                 |                 | 3  |
| 2  | `^^^^^^^^^^^^^` |                 |                 | 2  |
| 1  | `^^^^^^^^^^^^^` |                 |                 | 1  |

_*Rear-Mounted*_

| U  |     SETI Rack #8     | SETI Rack #9         | SETI Rack #10        | U  |
|:--:|:--------------------:|:--------------------:|:--------------------:|:--:|
| 42 | `cosmic-1g-switch-7` | `cosmic-1g-switch-8` | `cosmic-1g-switch-9` | 42 |
| 41 |                      |                      |                      | 41 |
| 40 |                      |                      |                      | 40 |
| 39 |                      |                      |                      | 39 |
| 38 |                      |                      |                      | 38 |
| 37 |                      |                      |                      | 37 |
| 36 |                      |                      |                      | 36 |
| 35 |                      |                      |                      | 35 |
| 34 |                      |                      |                      | 34 |
| 33 |                      |                      |                      | 33 |
| 32 |                      |                      |                      | 32 |
| 31 |                      |                      |                      | 31 |
| 30 |                      |                      |                      | 30 |
| 29 |                      |                      |                      | 29 |
| 28 |                      |                      |                      | 28 |
| 27 |                      |                      |                      | 27 |
| 26 |                      |                      |                      | 26 |
| 25 |                      |                      |                      | 25 |
| 24 |                      |                      |                      | 24 |
| 23 |                      |                      |                      | 23 |
| 22 |                      |                      |                      | 22 |
| 21 |                      |                      |                      | 21 |
| 20 |                      |                      |                      | 20 |
| 19 |                      |                      |                      | 19 |
| 18 |                      |                      |                      | 18 |
| 17 |                      |                      |                      | 17 |
| 16 |                      |                      |                      | 16 |
| 15 |                      |                      |                      | 15 |
| 14 |                      |                      |                      | 14 |
| 13 |                      |                      |                      | 13 |
| 12 |                      |                      |                      | 12 |
| 11 |                      |                      |                      | 11 |
| 10 |                      |                      |                      | 10 |
| 9  |                      |                      |                      | 9  |
| 8  |                      |                      |                      | 8  |
| 7  |                      |                      |                      | 7  |
| 6  |                      |                      |                      | 6  |
| 5  |                      |                      |                      | 5  |
| 4  |                      |                      |                      | 4  |
| 3  |                      |                      |                      | 3  |
| 2  |                      |                      |                      | 2  |
| 1  |                      |                      |                      | 1  |
