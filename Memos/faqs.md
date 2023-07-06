# COSMIC FAQs

## Creating New User Accounts (Head Node only)

1. Obtain the `$username` desired by the new user, and a public SSH key
2. On `cosmic-head`:
   ```
   sudo adduser $username
   sudo mkdir ~$username/.ssh
   sudo vim ~$username/.ssh/authorized_keys
   # Paste the public SSH key in this file
   sudo chown $username:$username ~$username/.ssh/authorized_keys
   sudo chmod 600 ~$username/.ssh/authorized_keys
   ```
3. If you wish to add the user to the netboot systems as well, on `cosmic-head`:
   ```
   # First get the User and group IDs of the account you just created
   grep $username /etc/passwd
   # returns something like: username:x:1019:1020:User Name,,,,:/home/username:/bin/bash
   # In this case, user ID is 1019, and group ID is 1020
   # Now, enter the netboot filesystem
   sudo nbroot
   groupadd -g <group ID> <username>
   adduser --uid <user ID> --gid <group ID> <username>
   # If this fails because the user/group ID are already in use, well, that's gonna need to be wrestled into submission :)
   ```
   

## Set up SSH keys

The following ssh config file (placed in `~/.ssh/config`) will allow you to ssh to the COSMIC head node with the command `ssh cosmic`, tunnelling through the VLA gateway machine. If you are connecting from within the NRAO network (where you should have direct access to `cosmic-head`, you can omit the `Proxyjump vla` entry.

```
Host vla
  HostName ssh.aoc.nrao.edu
  User <your NRAO username>
  PreferredAuthentications password
  PubkeyAuthentication no
  ForwardX11 yes

Host cosmic
  HostName cosmic-head
  User <your COSMIC username>
  ForwardX11 yes
  IdentityFile ~/.ssh/id_rsa
  Proxyjump vla
```

## Connect to a VNC

### One-time configuration
1. On `cosmic-head` configure the desktop
   ```
   mkdir ~/.vnc
   cp ~jackh/.vnc/xstartup ~/.vnc/
   ```

### Session startup

1. Start a VNC session
   ```
   vncserver -geometry 1700x900 # Or whatever geometry (specified in pixels) you want
   ```
   On the first run, you will be prompted to create a password.

2. Note the screen number you have been allocated:
   ```
   (py3venv) jackh@cosmic-head:~$ vncserver -geometry 1700x900
     
   New 'cosmic-head:4 (jackh)' desktop at :4 on machine cosmic-head

   Starting applications specified in /home/jackh/.vnc/xstartup
   Log file is /home/jackh/.vnc/cosmic-head:4.log

   Use xtigervncviewer -SecurityTypes VncAuth -passwd /home/jackh/.vnc/passwd :4 to connect to the VNC server.
   ```

   The above indicates a desktop has been started with ID `4`

3. From your local machine, connect to this desktop - you will have to tunnel. On linux:
   ```
   vncviewer -via cosmic :4 # Assuming you have an ssh config entry for `cosmic`
   ```
This will first prompt for an NRAO password, if you are tunneling through the NRAO ssh gateway, and then the VNC password.

## Powering up the System

In the event that the COSMIC system needs to be brought up from a full power down"

1. Power up `cosmic-head`, which can be remotely controlled from the NRAO netowork (eg. via `gygax`)
   ```
   # from gygax
   ipmitool -I lanplus -H cosmic-head-bmc -U ADMIN -P <IPMI-password> power up
   ```
2. Once `cosmic-head` is booted, turn on NAT if the COSMIC network needs internet access
   ```
   # on cosmic-head
   sudo ~cosmic/bin/nat on
   ```
4. Once `cosmic-head` is booted, other machines within the cosmic system can be started
   ```
   # from cosmic-head
   # power up storage nodes:
   for host in cosmic-storage-{1..2}-ipmi; do echo -n "${host}: "; ipmitool -I lanplus -U ADMIN -P <IPMI-password> -H $host power up; done
   # power up FPGA nodes:
   for host in cosmic-fpga-{0..2}-ipmi; do echo -n "${host}: "; ipmitool -I lanplus -U ADMIN -P <IPMI-password> -H $host power up; done
   # power up GPU nodes:
   for host in cosmic-gpu-{0..23}-ipmi; do echo -n "${host}: "; ipmitool -I lanplus -U ADMIN -P <IPMI-password> -H $host power up; done
   ```
5. If necessary, you can check whether a server is powered up with:
   ```
   ipmitool -I lanplus -U ADMIN -P <IPMI-password> -H <ipmi hostname> power status
   ``` 

## Remapping Antenna to F-Engines

There is one file that states the relationship between VLA antenna and COSMIC F-Engine Pipeline: `/home/cosmic/conf/antenna_fengine_mapping.yaml` on the `cosmic-head` node.
Updating this is all that is required. Note that the service running on the F-Engine servers has a configuration file that can exclude PCIe devices from being exposed via the service (by the PCIE_IGNORE value).
