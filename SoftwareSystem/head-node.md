# Preface

Some characteristic terms of the VLA are listed below:

- Time on the VLA instrument is divided into 'scans' during which the instrument's tuning, pointing and general operation defined.

# Overview

The background services that collectively give rise to COSMICs operation at the VLA are detailed below.

## mcast2redis

The VLA system communicates its state via MCAST packets: updates about scan configurations, physical antenna configuration and delay models all come through this. The [EVLA-MCAST](https://github.com/demorest/evla_mcast) python library is leveraged to capture this information and populate redis hashes with the meta-data in the [mcast2redis](https://github.com/COSMIC-SETI/COSMIC-VLA-PythonLibs/blob/main/scripts/mcast2redis.py) systemd service.

### Ingest Sources

Source | Provision
-|-
`/home/cosmic/conf/antenna_fengine_mapping.yaml` | The relationship between FPGAs, detailed as server-hostname/PCIe-ID/FPGA-pipeline-id, and the attached antenna, detailed by common name.
[evla_mcast.mcast_clients.ObsClient](https://github.com/demorest/evla_mcast/blob/master/evla_mcast/mcast_clients.py#L80) | The meta-data about contemporary VLA scans.
[evla_mcast.mcast_clients.AntClient](https://github.com/demorest/evla_mcast/blob/master/evla_mcast/mcast_clients.py#L121) | Updates about the phsyical antenna configuration.

### Egress Sources

Source | Provision
-|-
redis-hash:META_ANT, redis-hash:META_antennaProperties, redis-channel:meta_antennaproperties, `/home/cosmic/src/telinfo_vla.toml` | Physical antenna configuration.
redis-hash:META | Current VLA scan's meta-data.


