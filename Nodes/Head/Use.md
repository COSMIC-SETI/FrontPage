Also see:
- [Monitors](./Use-Monitors.md)
- [Services](./Use-Services.md)

# Context

All of these python scripts/commands are installed under the `cosmic` user, `cosmic_vla` conda environment.

```
...$ sudo su cosmic
(base) cosmic@cosmic-head:~/dev$ conda activate cosmic_vla
(cosmic_vla) cosmic@cosmic-head:~/dev$
```

# Starting up Hashpipe on the GPU Node(s)

Under `cosmic` user, execute the ansible-playbook of choice:

Playbook | Recording Mode Description
-|-
voltage_record | GUPPI RAW files, no processing.
xgpu_record | XGPU correlated UVH5 files.
beamformer_record | BLADE Beamformed RAW files. *Not tested!!*

```
(cosmic_vla)$ ansible-playbook ~cosmic/dev/FrontPage/Nodes/Head/ansible_playbooks/hashpipe/voltage_record.yml -K
```

![cosmic_head Starting Hashpipe](./images/cosmic_head_start_hashpipe.png)

As is evident from the playbook printout, hashpipe is compiled and the systemd services `hpguppi` and `redis_gateway` are restarted on the GPU-compute nodes.

# Configuration of the array's FEngines

First configure the FEngines (defaultly uses `~cosmic/dev/COSMIC-VLA-PythonLibs/scripts/vla_f_config.yaml` but one can specify a different configuration file with `--config-file`):
```
~cosmic/dev/COSMIC-VLA-PythonLibs/scripts$ python ./configure_remotefpga.py
```

**NOTE THAT THIS MUST BE RUN FROM THE `~cosmic/dev/COSMIC-VLA-PythonLibs/scripts` DIRECTORY!**

While the yaml file's contents are fairly static, one may wish to adjust the `antenna` and `chan_range` entries.
The `antenna` entry is an indented, bullet-point style list of the antenna names to configure.
The `chan_range` entry is a `[start, stop]` statement of the channel range to send to the encapsulating destination structure.

Configuration automatically publishes the configuration meta-data (NCHAN, NANTS etc) to the appropriate hashpipe instances. To do this manually (say if the instances are restarted but the FEngines are not reconfigured) run `publish_hashpipe_ingest_metadata.py`.

# Recording data with Hashpipe on the GPU Node(s)

Run `start_observation.py -i 5 -n 30`, where the former argument is the delay until observation start, and the latter is the observation duration, both in seconds.

# Troubleshooting

If it appears that the hashpipe backends are non-operational (DAQPULSE is stale, or the IBVGBPS doesn't match the expected GB/s), [restart them](#Starting_up_Hashpipe_on_th_GPU_Node(s)).

If the recording doesn't seem to go to plan, run `publish_hashpipe_ingest_metadata.py` before trying again, to ensure that hashpipe has the correct impression of the received data stream.
