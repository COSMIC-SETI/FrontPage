# Slack bot

The slack bot API requires a token, which is set as an environment variable for a few services. If the token changes, these are the locations where the update ought to propogate to.

File | Related service
-|-
`/home/cosmic/.bashrc` | Bash
`SLACK_BOT_TOKEN` environment variable in `obs_wait` screen under `cosmic` user | Observation control service.
`SLACK_BOT_TOKEN` environment variable in `obs_wait` screen under `cosmic` user | Observation control service.
`/home/cosmic/src/pypeline_stages/systemd_service/pypeline_service.conf` | Post-processing 'pypeline' instances on GPU nodes.
`/home/cosmic/src/COSMIC-VLA-DelayEngine/systemd-services/calibration_gain_collator.service` | Calibration collation service on head node.