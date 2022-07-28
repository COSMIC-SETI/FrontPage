## MCAST MetaData Monitor

The MCAST meta-data of the system is received by the (`~cosmic/Cosmic_VLA/Cosmic-VLA-RedisPub/mcast2redis.py`)[https://github.com/COSMIC-SETI/Cosmic-VLA-RedisPub/blob/main/mcast2redis.py] script, which populates hashes in REDIS. The script is typically running in the `mcast2redis` screen session, under the `cosmic` user. It is started with `(cosmic_vla) cosmic@cosmic-head:~/Cosmic_VLA$ python mcast2redis.py`.

The populated hashes of REDIS are displayed in a monitoring dashboard, served on port 8081 of the Head-Node. The dashboard is typically running under the `meta_monitor` screen session, under the `cosmic` user. It is started with `cosmic@cosmic-head:~/dev/vla_metakey_monitor$ node main.js`.

SSH-Tunneling of the related port will expose it on your local machine (localhost:8081 in your web-browser):
```
ssh username@login.aoc.nrao -L 8081:10.80.100.243:8081
```

## Monitoring the Hashpipe instances

There is a monitoring dashboard that is served on port 8082 of the Head-Node. It runs in the `hashpipe_monitor` screen session, under the `cosmic` user. It is started with `cosmic@cosmic-head:~/dev/atapipelinemonitor$ node ./main.js`.

SSH-Tunneling of the related port will expose it on your local machine (localhost:8082 in your web-browser):
```
ssh username@login.aoc.nrao -L 8082:10.80.100.243:8082
```