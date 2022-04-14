## Ansible for Playbook control of Hashpipe instances
All completed under the `cosmic` user.


#### SSH Key

Generate key pair.
```
ssh-key -t rsa -b 2048 -f /home/cosmic/.ssh/cosmic_id_rsa
```

Apply public key to `authorized_keys` of target host-user.
```
cat ~cosmic/.ssh/cosmic_id_rsa.pub | ssh cosmic@cosmic-gpu-0 "cat >> .ssh/authorized_keys"
```

#### Installation and setup

```
# apt install ansible
```

Add host pattern: `# nano /etc/ansible/hosts`
```
[cosmicnodes]
cosmic-gpu-0
```

Set SSH key to use: `# nano /etc/ansible/ansible.cfg` (Line 136)
```
private_key_file = /home/cosmic/.ssh/cosmic_id_rsa
```

Test
```
ansible cosmicnodes -m shell -a "df -h"
```