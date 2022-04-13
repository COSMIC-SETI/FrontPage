# COSMIC Compute Infrastructure
>13 April 2022, Jack Hickish

## Network Domains

### NRAO-wide “Public”

aoc.nrao.edu (Socorro operations center)
vla.nrao.edu (VLA site)

IPs from NRAO-controlled DHCP

Host (.aoc.nrao.edu) | IP | Notes
-|-|-
cosmic-dev1 | ?? |
cosmic-dev1-ipmi| 10.64.79.128 | 

Host (.vla.nrao.edu)|IP|Notes
-|-|-
setigw|10.80.100.243|Cosmic head node; aka cosmic-head (eno1np0)
setigw-bmc|??|COSMIC head node IPMI


### COSMIC “private” 1G domain. 192.168.32.0/24

1 GbE Control domain:
DHCP from cosmic-head (aka setigw) port eno2np1

Host|MAC|IP|Notes
-|-|-|-
cosmic-head|3c:ec:ef:78:76:9f|192.168.32.1|eno2np1
cosmic-100g-switch-0|70:0f:6a:96:f7:ec|192.168.32.20|
cosmic-pdu-0|28:29:86:46:c1:c4|192.168.32.30|
cosmic-pdu-1|28:29:86:46:c4:00|192.168.32.31|
cosmic-fpga-0|a0:42:3f:41:6d:56|192.168.32.100|FPGA host server
cosmic-fpga-1|a0:42:3f:41:6c:e4|192.168.32.101|FPGA host server
cosmic-fpga-2|a0:42:3f:3e:9a:d6|192.168.32.102|FPGA host server
cosmic-gpu-0|3c:ec:ef:05:9b:9e|192.168.32.110|GPU host
cosmic-fpga-0-ipmi|a0:42:3f:3f:6f:90|192.168.32.200|FPGA host server ipmi
cosmic-fpga-1-ipmi|TBC|192.168.32.201|FPGA host server ipmi
cosmic-fpga-2-ipmi|TBC|192.168.32.202|FPGA host server ipmi
cosmic-gpu-0-ipmi|3c:ec:ef:2f:0b:08|192.168.32.210|GPU host IPMI


### COSMIC 100G Domains (192.168.64.0/23)

#### GPU nodes port enp97s0f1 (192.168.64.0/24)

Host|IP|Notes
-|-|-
cosmic-gpu-0-100g-0|192.168.64.100|cosmic-gpu-0/enp97s0f1

#### GPU nodes port enp225s0f1 (192.168.65.0/24)

Host|IP|Notes
-|-|-
cosmic-gpu-0-100g-1|192.168.65.100|cosmic-gpu-0/enp225s0f1
