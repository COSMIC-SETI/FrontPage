# Overview

Data acquisition is foremostly accomplished with instances of hashpipe (instances are a collection of threads, which are developed under the [hpguppi_daq repository](https://github.com/MydonSolutions/hpguppi_daq/tree/seti-vla-8bit)). There after there is a [post-processing pipeline](#post-processing-pypeline) from which further data-products are accomplished.

Each compute node effects 2 computational instances as there are 2 sets of `{CPU, NIC, GPU, NVMe mount}` per node. The data pipelines follow this pattern and there are 2 active instances of the full pipeline set (`{hashpipe, pypeline}`) on each compute node. A second pair of the pipeline set is in-active and configured to effect the alternative data-process to expedite 'switches' in recording products.

The modes are configured in a yaml file (the path of which is passed as an argument within the [service](../Nodes/GPU-Compute/systemd_services/hpdaq.service)). The yaml file also provides initial values for some critical status key-values. The [yaml file in use](https://github.com/MydonSolutions/hpguppi_daq/blob/seti-vla-8bit/src/config_hpguppi.yml) is a part of the hpguppi_daq repository.

# Hashpipe

Hashpipe is a framework in which 'threads' are tied together to form a pipeline, with the threads passing 'databuffers' down-stream.

There are 2 production pipelines in use for the purposes of COSMIC: a correlation pipeline and a GUPPI RAW pipeline. 

## Correlation Pipeline

The correlation pipeline has a thread that employs xGPU to provide baseline correlations polarity-products.

A single `.uvh5` file is produced.

### Runtime Parameters

The following key-values can be set in the hashpipe status-buffer to affect the correlation pipeline. Note that the typical place to do this is in the [observation yaml specification](./subsys_observation_control.md#cosmic-observations) (under `hashpipe_keys`).

Title | Key-Value Pair | Description | Source (default)
-|-|-
Integration Time | `XTIMEINT` as seconds | The timespan to be integrated (internally rounded up to nearest appropriate multiple, and updated). | Observation client (0.0)
Project ID | `PROJID` as a string | The first sub-directory under the `DATADIR` of the file-path. | Observation client (`xgpu`)
Polarities String | `POLS` as a string | A string where each character symbolises the polarities present, in order. Character set is {x, y, r, l}. | config_hpguppi.yaml (`rl`)
Telescope Info TOML Filepath | `UVH5TELP` as a string | The UVH5 library accesses this, primarily to gain the antenna positions. | config_hpguppi.yaml (/home/cosmic/conf/telinfo_vla.toml)
Number of GPU Integrations | `XGPU` as an integer | This many of the integrations are performed by xGPU on the GPU (which accumulates in 32-bit integers). | config_hpguppi.yaml (1)

## GUPPI RAW Pipeline

The GUPPI RAW pipeline merely writes the collective data-stream to disk in the GUPPI RAW format, where each block's header is the hashpipe's status-buffer.

Multiple `.\d{4}.raw` part-files are produced.

### User Controlled Runtime Parameters

The following key-values can be set in the hashpipe status-buffer to affect the GUPPI RAW pipeline. Note that the typical place to do this is in the [observation yaml specification](./subsys_observation_control.md#cosmic-observations) (under `hashpipe_keys`).

Title | Key-Value Pair | Description
-|-|-
Project ID | `PROJID` as a string | The first sub-directory under the `DATADIR` of the file-path.


# Post-Processing 'pypeline'

Each instance of hashpipe has a corresponding [`pypeline`](https://github.com/MydonSolutions/hpguppi_pypeline) instance which is a framework in which python scripts (called 'stages') are tied together.

The operation of a pypeline instance is configured via its associated redis interface. [Typical post-processes](https://github.com/COSMIC-SETI/active_observations/blob/main/postprocesses.json) are to calibrate using the correlation mode's UVH5 product and to beamform and signal-search the RAW mode's GUPPI RAW files.
