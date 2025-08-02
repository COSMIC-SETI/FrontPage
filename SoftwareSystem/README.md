# Sub-systems

The COSMIC system is setup to search for signals in data beamformed from upchannelized antenna data. The primary goal is to have data-acquisition, beamform-search and archival happen automatically for the appropriate VLA scans. Similarly the calibration scans are also to be used to calibrate the COSMIC system. To these ends there are the following sub-systems:

- [Observation control](./subsys_observation_control.md)
- [Calibration system](https://github.com/COSMIC-SETI/COSMIC-VLA-CalibrationEngine#readme)
- [Data acquisition and post-processing](./subsys_data_acquisition.md)
- [Delay tracking system](https://github.com/COSMIC-SETI/COSMIC-VLA-DelayEngine#readme)
- [Beamform-search pipeline](./subsys_BLADE.md)
- [Data archival](./subsys_data_archival.md)

# Indices

- [Redis](./index_redis.md)
- [Systemd Services](./index_systemd.md)
- [Slack Bot](./index_slackbot.md)

# Troubleshooting

- [Overall](./troubleshooting.md)