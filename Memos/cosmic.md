# COSMIC Top-Level System Description

## Introduction

COSMIC (The _Commensal, Open-Source, Multi-mode Interferometer Cluster_) is a real-time digital signal processing system, implemented on a cluster of Field Programmable Gate Arrays (FPGAs) and off-the-shelf GNU/Linux servers accelerated by GPU cards.
COSMIC is fed by a copy of the digitized data streams transmitted from each VLA antenna, such that the system can operate concurrantly with the VLA facility correlator, WIDAR.
The COSMIC DSP pipeline searches VLA data for narrowband (~1 Hz) signals which may be drifting in frequency over time.
A high-level depiction of COSMIC processing steps is shown below.

|![cosmic\_dataflow](./_figures/COSMIC_Dataflow.png)|
|:--:|
| *A high-level representation of data flow in the COSMIC system. Digitized data streams from each VLA antenna are amplified and split, with one copy feeding the COSMIC DSP pipeline and the other feeding WIDAR. The COSMIC frontend DSP pipeline channelizes (using FPGAs) data streams to 1 MHz resolution, and then distributes channels over multiple backend DSP pipelines (implemented on CPU/GPUs). Backend pipelines further channelize to ~1 Hz resolution, and search for narrowband drifting signals. When signals are detected, the per-antenna, 1 Hz voltages are archived around the time-frequency extent of the detected signal.* |

While this pipeline is conceptually simple, the practical implementation is complicated.
In addition to the signal processing tasks (i.e., upchannelizing, doppler searching, etc.) the system must also:

 - Monitor what the VLA antennas are doing -- where they are pointed, how receivers are tuned.
 - Calculate (using appropriate commensal observations) calibration gains for each antenna.
 - Choose, and track, a fixed phase-center over the coarse of a search pipeline execution.
 - Generate appropriate beam co-ordinates, and use these to derive beamforming coefficients
 - Archive results in a searchable fashion, with tracable records of system performance.

These tasks are in addition to the more mundane monitoring and control of a multi-node FPGA/CPU/GPU processing cluster.
This document attempts to provide a high-level overview of how COSMIC accomplishes these tasks, and how the many software processes in the COSMIC system interact with one another.
It also serves as a reference for hardware models, and locations of code repositories.

## Hardware

To the greatest extent possible, all hardware used in COSMIC is off-the-shelf.

### Optical Hardware

The optical frontend of COSMIC comprises optical Erbium-Doped Fiber Amplifliers (EDFAs), optical splitters, patch panels, and Dense Wavelength-Division Multiplexing (DWDM) demultiplexers.
All but the latter are formally owned by the National Radio Astronomy Observatory (NRAO).

All optical hardware was sourced from [Fiberstore](http://www.fs.com).

| Manufacturer | Model | Required | Spares |
| -- | -- | -- | -- | -- |
| Fiberstore | [M6200-CH2U](https://www.fs.com/products/107371.html) | 28 | 7 |
| Fiberstore | [M6200-SFPVOA](https://www.fs.com/products/107373.html) | 28 | 7 |
| Fiberstore | [M6200-25PA](https://www.fs.com/products/107367.html) | 28 | 1 |

|![cosmic\_fiber](./_figures/COSMIC_Fiber.png)|
|:--:|
| *The COSMIC optical frontend. NRAO-owned equipment is shown in blue. SETI-Institute-owned equipent is shown in red.* |

### FPGAs

### CPU/GPU servers

### Storage Servers

### Head node

### Networking

### System Layout

## System Behaviour

 1. Observations are specified in `YAML` files, which define system behaviour associated with a particular VLA telescope state.

## Software

### COSMIC Services



