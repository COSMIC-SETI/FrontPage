# Adding mounts
## Head-Node 

The head-node uses fstab. Copy one of the final lines and alter accordingly:
```
tail /etc/fstab -n 12 | head -n 3
# Storage servers
192.168.32.111:/srv/data0 /mnt/cosmic-gpu-1/data0 nfs rw,hard,nointr,nofail,nfsvers=3 0 0
192.168.32.105:/srv/data0 /mnt/cosmic-storage-1/data0 nfs rw,hard,nointr,nofail,nfsvers=3 0 0
```

Create the mount directory, with permissions:
`sudo mkdir /mnt/cosmic-storage-1/data3`
`sudo chmod a+w /mnt/cosmic-storage-1/data3`

Refresh the fstab:
`sudo mount -a`

## Compute-Nodes
The compute-nodes use autofs... :shrug: