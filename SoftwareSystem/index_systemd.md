# COSMIC Services

The top-level executables for each sub-system are preferably wrapped up as systemd services so that there is a uniform initiation, configuration and start-automation protocol.

## `cosmic-head` Node Services

Systemd Service | Configuration File | Description
-|-|-
[mcast2redis](https://github.com/COSMIC-SETI/Cosmic-VLA-PythonLibs/blob/main/systemd-services/mcast2redis.service) | | Gather VLA mcast xml information and populate COSMIC files and redis hashes, channels.
[flaggedantenna](https://github.com/COSMIC-SETI/Cosmic-VLA-PythonLibs/blob/main/systemd-services/flaggedantenna.service) | | Poll VLA antenna-flags server and populate COSMIC redis hash.
[hashpipe_meta_marshall](https://github.com/COSMIC-SETI/Cosmic-VLA-PythonLibs/blob/main/systemd-services/hashpipe_meta_marshall.service) | | Poll VLA antenna-flags server and populate COSMIC redis hash.
[phase_center_controller](https://github.com/COSMIC-SETI/COSMIC-VLA-PythonLibs/blob/main/systemd-services/phase_center_controller.service) | | Set phase-center to boresight for non-OTF scans and to the running slewed position for OTF scans.
vla_metakey_monitor | | Serve an HTML dashboard of the COSMIC configuration redis hashes, on port 8081.
[hashpipe_monitor](https://github.com/MydonSolutions/atapipelinemonitor/blob/vla_cosmic/systemd-services/hashpipe_monitor.service) | | Serve an HTML dashboard of the hashpipe status-buffers for all instances, on port 8082.
vla_metakey_monitor | | Serve an HTML dashboard of the redis hashes.
[target_selector](https://github.com/COSMIC-SETI/targets-minimal/blob/cosmic/systemd_service/target_selector.service) | `/home/cosmic/conf/targetselector_mysql_conf.yml` | Serve target coordinates at which to beamform.


## `cosmic-gpu-*` Node Services

Systemd Service | Configuration File | Description
-|-|-
[hpdaq](../Nodes/GPU-Compute/systemd_services/hpdaq.service) | [`/home/cosmic/hpdaq_service.conf`](../Nodes/GPU-Compute/systemd_services/hpdaq_service.conf) | The {0, 1} pair of hashpipe instances.
[hpdaq_secondary](../Nodes/GPU-Compute/systemd_services/hpdaq_secondary.service) | [`/home/cosmic/hpdaq_service.conf`](../Nodes/GPU-Compute/systemd_services/hpdaq_service.conf) | The {2, 3} pair of hashpipe instances.
[pypeline@?](https://github.com/COSMIC-SETI/pypeline_stages/blob/main/systemd_service/pypeline%40.service) | [`/home/cosmic/src/pypeline_stages/systemd_service/pypeline_service.conf`](https://github.com/COSMIC-SETI/pypeline_stages/blob/main/systemd_service/pypeline_service.conf) | The pypeline instances for post-processing ({0, 1, 2, 3}).

## `cosmic-fpga-*` Node Services

Systemd Service | Configuration File | Description
-|-|-
[remoteobjects_server](../Nodes/FPGA/systemd_services/remoteobjects_server.service) | [`/home/cosmic/remoteobjects_server.conf`](../Nodes/FPGA/systemd_services/remoteobjects_server.conf) | The REST server exposing the local FPGA PCIe devices.