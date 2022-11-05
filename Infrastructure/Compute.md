# COSMIC Compute Infrastructure
>13 April 2022, Jack Hickish

## Network Domains

### NRAO-wide “Public”

aoc.nrao.edu (Socorro operations center)
vla.nrao.edu (VLA site)

IPs from NRAO-controlled DHCP

Host (.aoc.nrao.edu) | IP | Notes
-|-|-
cosmic-dev1 | ?? |Not sure these names
cosmic-dev1-ipmi| 10.64.79.128 |still exist in aoc.nrao.edu

Host (.vla.nrao.edu)|IP/Subnet|Notes
-|-|-
cosmic-head|10.80.253.243/24|Cosmic head node; formerly known as setigw (eno1np0)
cosmic-head-bmc|10.80.253.242/24|COSMIC head node IPMI


### COSMIC “private” 1G domain. 192.168.32.0/23

Number of hosts anticipated: 1 x headnode + 128 x Compute + "a few" storage / axiliary

Number of IPMI hosts anticipated: 1 x headnode + 128 x Compute + "a few" storage / axiliary

Total: 256 + "a few"


#### 1 GbE IP Address Ranges

IP First|IP Last|Control
-|-|-
192.168.32.1|192.168.32.19|No DHCP, manually administered
192.168.32.20|192.168.33.239|Static DHCP from cosmic-head:eno2np1 (i.e. known MACs)
192.168.33.240|192.169.33.254|Dynamic DHCP from cosmic-head:eno2np1 (i.e. unknown MACs)

IP addresses in the range `192.168.33.240` to `192.168.33.254` are dynamically
assigned to unknown MAC addresses to accommodate laptops or other ad hoc
devices that may be temporarily connected for development/diagnostic purposes.

#### 1 GbE IP Address Map

Host (.cosmic.pvt) |MAC|IP|Notes
-|-|-|-
cosmic-head|3c:ec:ef:78:76:9f|192.168.32.1|eno2np1
cosmic-100g-switch-0|70:0f:6a:96:f7:ec|192.168.32.20|100 GbE switch
cosmic-100g-switch-1||192.168.32.21|100 GbE switch, Note 1
cosmic-pdu-0|28:29:86:46:c1:c4|192.168.32.30|SETI Rack #1
cosmic-pdu-1|28:29:86:46:c4:00|192.168.32.31|SETI Rack #2
cosmic-pdu-2||192.168.32.32|SETI Rack #3, Note 2
cosmic-pdu-3||192.168.32.33|SETI Rack #4, Note 2
cosmic-pdu-4||192.168.32.34|SETI Rack #5, Note 2
cosmic-pdu-5||192.168.32.35|SETI Rack #6, Note 2
cosmic-pdu-6||192.168.32.36|SETI Rack #7, Note 2
cosmic-pdu-7||192.168.32.37|SETI Rack #8, Note 2
cosmic-pdu-8||192.168.32.38|SETI Rack #9, Note 2
cosmic-pdu-9||192.168.32.39|SETI Rack #10, Note 2
cosmic-fpga-0|a0:42:3f:41:6d:56|192.168.32.100|FPGA host server
cosmic-fpga-1|a0:42:3f:41:6c:e4|192.168.32.101|FPGA host server
cosmic-fpga-2|a0:42:3f:3e:9a:d6|192.168.32.102|FPGA host server
cosmic-gpu-0|3c:ec:ef:05:9b:9e|192.168.32.110|GPU host
cosmic-gpu-1|04:42:1a:1b:0b:92|192.168.32.111|GPU host, Note 3
cosmic-gpu-2||192.168.32.112|GPU host, Note 2
cosmic-gpu-3||192.168.32.113|GPU host, Note 2
cosmic-gpu-4||192.168.32.114|GPU host, Note 2
cosmic-gpu-5||192.168.32.115|GPU host, Note 2
cosmic-gpu-6||192.168.32.116|GPU host, Note 2
cosmic-gpu-7||192.168.32.117|GPU host, Note 2
cosmic-gpu-8||192.168.32.118|GPU host, Note 2
cosmic-gpu-9||192.168.32.119|GPU host, Note 2
cosmic-gpu-10||192.168.32.120|GPU host, Note 2
cosmic-gpu-11||192.168.32.121|GPU host, Note 2
cosmic-gpu-12||192.168.32.122|GPU host, Note 2
cosmic-gpu-13||192.168.32.123|GPU host, Note 2
cosmic-gpu-14||192.168.32.124|GPU host, Note 2
cosmic-gpu-15||192.168.32.125|GPU host, Note 2
cosmic-gpu-16||192.168.32.126|GPU host, Note 2
cosmic-gpu-spare-0||TBD|GPU host, Note 2
cosmic-1g-switch-0|10:4f:58:bd:6c:e0|192.168.33.30|1 GbE switch, SETI Rack #1, Note 4
cosmic-1g-switch-1|10:4f:58:bd:4c:e0|192.168.33.31|1 GbE switch, SETI Rack #2, Note 5
cosmic-1g-switch-2||192.168.33.32|1 GbE switch, SETI Rack #3, Note 2
cosmic-1g-switch-3||192.168.33.33|1 GbE switch, SETI Rack #4, Note 2
cosmic-1g-switch-4||192.168.33.34|1 GbE switch, SETI Rack #5, Note 2
cosmic-1g-switch-5||192.168.33.35|1 GbE switch, SETI Rack #6, Note 2
cosmic-1g-switch-6||192.168.33.36|1 GbE switch, SETI Rack #7, Note 2
cosmic-1g-switch-7||192.168.33.37|1 GbE switch, SETI Rack #8, Note 2
cosmic-1g-switch-8||192.168.33.38|1 GbE switch, SETI Rack #9, Note 2
cosmic-1g-switch-9||192.168.33.39|1 GbE switch, SETI Rack #10, Note 2
cosmic-fpga-0-ipmi|a0:42:3f:3f:6f:90|192.168.33.100|FPGA host server ipmi
cosmic-fpga-1-ipmi|a0:42:3f:3f:6f:b4|192.168.33.101|FPGA host server ipmi
cosmic-fpga-2-ipmi|a0:42:3f:3d:2b:26|192.168.33.102|FPGA host server ipmi
cosmic-gpu-0-ipmi|3c:ec:ef:2f:0b:08|192.168.33.110|GPU host IPMI
cosmic-gpu-1-ipmi|04:42:1a:1b:0b:94|192.168.33.111|GPU host IPMI, Note 6
cosmic-gpu-2-ipmi||192.168.33.112|GPU host IPMI, Note 2
cosmic-gpu-3-ipmi||192.168.33.113|GPU host IPMI, Note 2
cosmic-gpu-4-ipmi||192.168.33.114|GPU host IPMI, Note 2
cosmic-gpu-5-ipmi||192.168.33.115|GPU host IPMI, Note 2
cosmic-gpu-6-ipmi||192.168.33.116|GPU host IPMI, Note 2
cosmic-gpu-7-ipmi||192.168.33.117|GPU host IPMI, Note 2
cosmic-gpu-8-ipmi||192.168.33.118|GPU host IPMI, Note 2
cosmic-gpu-9-ipmi||192.168.33.119|GPU host IPMI, Note 2
cosmic-gpu-10-ipmi||192.168.33.120|GPU host IPMI, Note 2
cosmic-gpu-11-ipmi||192.168.33.121|GPU host IPMI, Note 2
cosmic-gpu-12-ipmi||192.168.33.122|GPU host IPMI, Note 2
cosmic-gpu-13-ipmi||192.168.33.123|GPU host IPMI, Note 2
cosmic-gpu-14-ipmi||192.168.33.124|GPU host IPMI, Note 2
cosmic-gpu-15-ipmi||192.168.33.125|GPU host IPMI, Note 2
cosmic-gpu-16-ipmi||192.168.33.126|GPU host IPMI, Note 2
cosmic-gpu-spare-0-ipmi||TBD|GPU host IPMI, Note 2

Note 1: Installed, but management interface not cabled/configured  
Note 2: Not yet installed  
Note 3: This system will get canonical name `asusg0` and change to logical name `cosmic-fpga-spare-0`  
Note 4: As of 2022-11-04, still using arbitrary DHCP IP 192.168.32.229  
Note 5: As of 2022-11-04, still using arbitrary DHCP IP 192.168.32.226  
Note 6: This system will get canonical name `asusg0-ipmi` and change to logical name `cosmic-fpga-spare-0-ipmi`  

### COSMIC 100G Domains (192.168.64.0/23)

Number of hosts anticipated: 256 Compute + "a few" storage / axiliary

#### GPU nodes port enp97s0f1 (192.168.64.0/24)

Number of hosts anticipated: 128 Compute + "a few" storage / axiliary

Host|IP|Notes
-|-|-
cosmic-gpu-0-100g-0|192.168.64.100|cosmic-gpu-0/enp97s0f1

#### GPU nodes port enp225s0f1 (192.168.65.0/24)

Number of hosts anticipated: 128 Compute + "a few" storage / axiliary

Host|IP|Notes
-|-|-
cosmic-gpu-0-100g-1|192.168.65.100|cosmic-gpu-0/enp225s0f1
