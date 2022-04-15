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
(cosmic_vla) cosmic@cosmic-head:~/dev$ ansible-playbook ~cosmic/dev/ATA_ansible_playbooks/hashpipe/voltage_record.yml -K
```

![cosmic_head Starting Hashpipe](./images/cosmic_head_start_hashpipe.png)

## Recording data with Hashpipe on the GPU Node(s)

Under the `cosmic` user, `cosmic_vla` conda environment.
```
...$ sudo su cosmic
(base) cosmic@cosmic-head:~/dev$ conda activate cosmic_vla
(cosmic_vla) cosmic@cosmic-head:~/dev$
```

First configure the FEngines (statically uses `/home/cosmic/dev/observation_control/fengine_control/vla_f_config.yaml`):
```
python /home/cosmic/dev/observation_control/fengine_control/configure_remotefpga.py
```

See `configure_remotefpga.py -h` for more info. It automatically publishes the configuration meta-data (NCHAN, NANTS etc) to the appropriate hashpipe instances. To do this manually run `python /home/cosmic/dev/observation_control/fengine_control/feng_meta_marshal.py`.

Finally, run `python /home/cosmic/dev/observation_control/start_observation.py -i 5 -n 30`, where the former argument is the delay until observation start, and the latter is the observation duration, in seconds.