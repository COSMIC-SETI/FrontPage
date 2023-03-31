# Overview

Data acquisition is foremostly accomplished with instances of [hashpipe](https://github.com/MydonSolutions/hpguppi_daq/tree/seti-vla-8bit). There after there is a post-processing pipeline from which further data-products are accomplished.

Each compute node effects 2 computational instances as there are 2 sets of `{CPU, NIC, GPU, NVMe mount}` per node. The data pipelines follow this pattern and there are 2 active instances of the full pipeline set (`{hashpipe, pypeline}`) on each compute node. A second pair of the pipeline set is in-active and configured to effect the alternative data-process to expedite 'switches' in recording products.

# Hashpipe

Hashpipe is a framework in which 'threads' are tied together to form a pipeline, with the threads passing 'databuffers' down-stream.

There are 2 production pipelines in use for the purposes of COSMIC: a correlation pipeline and a GUPPI RAW pipeline. 

## Correlation Pipeline

The correlation pipeline has a thread that employs xGPU to provide baseline correlations polarity-products.

A single `.uvh5` file is produced.

### User Controlled Runtime Parameters

The following key-values can be set in the hashpipe status-buffer to affect the correlation pipeline:

Title | Key-Value Pair | Description
-|-|-
Integration Time | `XTIMEINT` as seconds | The timespan to be integrated (internally rounded up to nearest appropriate multiple, and updated).
Polarities String | `POLS` as a string | A string where each character symbolises the polarities present, in order. Character set is {x, y, r, l}, and for the VLA defaults to `rl`.
Project ID | `PROJID` as a string | The first sub-directory under the `DATADIR` of the file-path.


## GUPPI RAW Pipeline

The GUPPI RAW pipeline merely writes the collective data-stream to disk in the GUPPI RAW format, where each block's header is the hashpipe's status-buffer.

Multiple `.\d{4}.raw` part-files are produced.

### User Controlled Runtime Parameters

The following key-values can be set in the hashpipe status-buffer to affect the GUPPI RAW pipeline:

Title | Key-Value Pair | Description
-|-|-
Project ID | `PROJID` as a string | The first sub-directory under the `DATADIR` of the file-path.


# Post-Processing 'pypeline'

Each instance of hashpipe has a corresponding [`pypeline`](https://github.com/MydonSolutions/hpguppi_pypeline) instance which is a framework in which python scripts (called 'stages') are tied together.

The operation of a pypeline instance is configured via its associated redis interface. [Typical post-processes](https://github.com/COSMIC-SETI/active_observations/blob/main/postprocesses.json) are to calibrate using the correlation mode's UVH5 product and to beamform and signal-search the RAW mode's GUPPI RAW files.
