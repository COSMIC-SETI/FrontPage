## Redis-Server

The Redis-Server hosted on the Head-Node is wrapped in the `redis_server` systemd service. Use `sudo systemctl start/stop/restart/status redis_server` as is necessary.

## MCAST MetaData Monitor

The MCAST meta-data of the system is received by the (`~cosmic/Cosmic_VLA/Cosmic-VLA-RedisPub/mcast2redis.py`)[https://github.com/COSMIC-SETI/Cosmic-VLA-RedisPub/blob/main/mcast2redis.py] script, which populates hashes in REDIS. The script is typically running in the `mcast2redis` screen session, under the `cosmic` user. It is started with `(cosmic_vla) cosmic@cosmic-head:~/Cosmic_VLA$ python mcast2redis.py`.

The populated hashes of REDIS are displayed in a monitoring dashboard, served on port 8081 of the Head-Node. The dashboard is typically running under the `meta_monitor` screen session, under the `cosmic` user. It is started with `cosmic@cosmic-head:~/dev/vla_metakey_monitor$ node main.js`.

SSH-Tunneling of the related port will expose it on your local machine (localhost:8081 in your web-browser):
```
ssh username@login.aoc.nrao -L 8081:10.80.100.243:8081
```

## Starting up Hashpipe on the GPU Node(s)

Under `cosmic` user, execute the ansible-playbook of choice:

Playbook | Recording Mode Description
-|-
voltage_record | GUPPI RAW files, no processing.
xgpu_record | XGPU correlated UVH5 files.
beamformer_record | BLADE Beamformed RAW files. *Not tested!!*

```
$ sudo su cosmic
(base) cosmic@cosmic-head:~/dev$ conda activate cosmic_vla
(cosmic_vla) cosmic@cosmic-head:~/dev$ ansible-playbook ~cosmic/dev/FrontPage/Nodes/Head/ansible_playbooks/hashpipe/voltage_record.yml -K
```

![cosmic_head Starting Hashpipe](./images/cosmic_head_start_hashpipe.png)

As is evident from the playbook printout, hashpipe is compiled and the systemd services `hpguppi` and `redis_gateway` are restarted on the GPU-compute nodes.

## Monitoring the Hashpipe instances

There is a monitoring dashboard that is served on port 8082 of the Head-Node. It runs in the `hashpipe_monitor` screen session, under the `cosmic` user. It is started with `cosmic@cosmic-head:~/dev/atapipelinemonitor$ node ./main.js`.

SSH-Tunneling of the related port will expose it on your local machine (localhost:8082 in your web-browser):
```
ssh username@login.aoc.nrao -L 8082:10.80.100.243:8082
```

## Recording data with Hashpipe on the GPU Node(s)

Under the `cosmic` user, `cosmic_vla` conda environment.
```
...$ sudo su cosmic
(base) cosmic@cosmic-head:~/dev$ conda activate cosmic_vla
(cosmic_vla) cosmic@cosmic-head:~/dev$
```

First configure the FEngines (statically uses `~cosmic/dev/COSMIC-VLA-PythonLibs/scripts/vla_f_config.yaml`):
```
python configure_remotefpga.py
```

See `configure_remotefpga.py -h` for more info. It automatically publishes the configuration meta-data (NCHAN, NANTS etc) to the appropriate hashpipe instances. To do this manually run `publish_hashpipe_ingest_metadata.py`.

Finally, run `start_observation.py -i 5 -n 30`, where the former argument is the delay until observation start, and the latter is the observation duration, both in seconds.

If the recording doesn't seem to go to plan, run `publish_hashpipe_ingest_metadata.py` before trying again, to ensure that hashpipe has the correct impression of the received data stream.
