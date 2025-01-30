# Troubleshooting

## Check the NIC status of the GPU nodes
From the head-node:

```
ansible cosmicgpu -m shell -a "ip add show | grep -P \"eth2:|eth4:\" -A1"
```

## The switch is not correctly forwarding packets from the FEngines to the GPU nodes
Some development work on the FEngines can cause packets to be emitted with bogus MAC address destinations, which
fills up the related table in the NIC impeding its ability to route packets even when they are properly formed.

On the symptomatic switch:

```
show mac address-table
clear mac address-table dynamic
```