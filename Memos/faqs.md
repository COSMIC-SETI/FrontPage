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
