# redis

The [redis server](../Nodes/Head/systemd_services/README.md#redis) is used to provide the interfaces to many of COSMIC's sub-systems.

# Redis hashes

Hash | Written by | Read by | Description
-|-|-|-
META | `mcast2redis.service` | `observe.py`, `hashpipe_meta_marshall.service` | The VLA `scan` meta-data.
META_antennaProperties | `mcast2redis.service` | | The VLA's publication of antenna details combined with COSMIC's URI to the associated FPGA device.

# Redis channels

Hash | Published to by | Subscribed to by | Description
-|-|-|-
meta_obs | `mcast2redis.service` | `vlass_phase_center_controller.service` | The VLA `scan` meta-data, published at the start of a scan.
meta_antennaProperties | `mcast2redis.service` | | The VLA's publication of antenna details combined with COSMIC's URI to the associated FPGA device.
