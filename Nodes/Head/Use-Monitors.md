## MCAST MetaData Monitor

The MCAST meta-data of the system is received by the (`COSMIC-VLA-PythonLibs/scripts/mcast2redis.py`)[https://github.com/COSMIC-SETI/Cosmic-VLA-PythonLibs/blob/main/scripts/mcast2redis.py] script, which populates hashes in REDIS. It runs under th `mcast2redis` systemd service.

The populated hashes of REDIS are displayed in a monitoring dashboard, served on port 8081 of the Head-Node. The dashboard is typically running under the `vla_metakey_monitor` systemd service.

SSH-Tunneling of the related port will expose it on your local machine (localhost:8081 in your web-browser):
```
ssh username@login.aoc.nrao -L 8081:cosmic-head:8081
```

## Monitoring the Hashpipe instances

There is a monitoring dashboard that is served on port 8082 of the Head-Node. It runs in the `hashpipe_monitor` systemd service.

SSH-Tunneling of the related port will expose it on your local machine (localhost:8082 in your web-browser):
```
ssh username@login.aoc.nrao -L 8082:10.80.100.243:8082
```