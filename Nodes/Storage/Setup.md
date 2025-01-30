# Rsync Daemon 

```
$ sudo echo '
address = 
[data0]
  path = /srv/data0
  read only = false
[data1]
  path = /srv/data1
  read only = false
[data2]
  path = /srv/data2
  read only = false' > /etc/rsyncd.conf
```