# COSMIC Compute Infrastructure
>13 April 2022, Jack Hickish

## Network Domains

### NRAO-wide “Public”

aoc.nraddo.edu (Socorro operations center)
vla.nrao.edu (VLA site)

IPs from NRAO-controlled DHCP

Host (.vla.nrao.edu) | MAC | IP/Subnet | Notes
-|-|-|-
cosmic-head     | 3c:ec:ef:78:76:9e | 10.80.253.243/24 | Cosmic head node; formerly known as setigw (eno1np0)
cosmic-head-bmc | 3c:ec:ef:78:77:d7 | 10.80.253.242/24 | COSMIC head node IPMI
cosmic-pdu-0 | 28:29:86:46:c4:00 | 10.80.253.230/24 |SETI Rack #1
cosmic-pdu-1 | 28:29:86:46:c1:c4 | 10.80.253.231/24 |SETI Rack #2
cosmic-pdu-2 | 28:29:86:6b:ca:fd | 10.80.253.232/24 |SETI Rack #3
cosmic-pdu-3 | 28:29:86:6b:c3:58 | 10.80.253.233/24 |SETI Rack #4
cosmic-pdu-4 | 28:29:86:6b:c3:86 | 10.80.253.234/24 |SETI Rack #5
cosmic-pdu-5 | 28:29:86:6b:ca:33 | 10.80.253.235/24 |SETI Rack #6
cosmic-pdu-6 | TBC | 10.80.254.236 | SETI Rack #7, Note 1
cosmic-pdu-7 | TBC | 10.80.254.237 | SETI Rack #8, Note 1
cosmic-pdu-8 | TBC | 10.80.254.238 | SETI Rack #9, Note 1
cosmic-pdu-9 | TBC | 10.80.254.239 | SETI Rack #10, Note 1


### COSMIC “private” 1G domain. 192.168.32.0/23

Number of hosts anticipated: 1 x headnode + 128 x Compute + "a few" storage / auxiliary

Number of IPMI hosts anticipated: 1 x headnode + 128 x Compute + "a few" storage / auxiliary

Total: 256 + "a few"


#### 1 GbE IP Address Ranges

IP First | IP Last | Control
-|-|-
192.168.32.1   | 192.168.32.19  | No DHCP, manually administered
192.168.32.20  | 192.168.33.239 | Static DHCP from cosmic-head:eno2np1 (i.e. known MACs)
192.168.33.240 | 192.169.33.254 | Dynamic DHCP from cosmic-head:eno2np1 (i.e. unknown MACs)

IP addresses in the range `192.168.33.240` to `192.168.33.254` are dynamically
assigned to unknown MAC addresses to accommodate laptops or other ad hoc
devices that may be temporarily connected for development/diagnostic purposes.

#### 1 GbE IP Address Map

Host (.cosmic.pvt)  | MAC | IP | Notes
-|-|-|-
cosmic-head | 3c:ec:ef:78:76:9f | 192.168.32.1 | eno2np1
cosmic-100g-switch-0 | 70:0f:6a:96:f7:ec | 192.168.32.20 | 100 GbE switch, Rack #1
cosmic-100g-switch-1 | 70:ea:1a:53:7b:56 | 192.168.32.21 | 100 GbE switch, Rack #1
cosmic-fpga-0 | a0:42:3f:41:6d:56 | 192.168.32.100 | FPGA host server, Rack #1
cosmic-fpga-1 | a0:42:3f:41:6c:e4 | 192.168.32.101 | FPGA host server, Rack #1
cosmic-fpga-2 | a0:42:3f:3e:9a:d6 | 192.168.32.102 | FPGA host server, Rack #1
cosmic-storage-1 | 3c:ec:ef:91:65:6c | 192.168.32.105 | Storage server, Rack #2
cosmic-storage-2 | 3c:ec:ef:91:54:e4 | 192.168.32.106 | Storage server, Rack #2
cosmic-gpu-0 | 3c:ec:ef:05:9b:9e | 192.168.32.110 | GPU host, Rack #2
cosmic-gpu-1 | 04:42:1a:1b:0b:92 | 192.168.32.111 | GPU host, Rack #2, 2U asus box (canonical name `asusg0`)
cosmic-gpu-2 | 3c:ec:ef:f2:fc:72 | 192.168.32.112 | GPU host, Rack #3
cosmic-gpu-3 | 7c:c2:55:14:ef:e4 | 192.168.32.113 | GPU host, Rack #3
cosmic-gpu-4 | 7c:c2:55:14:ef:fa | 192.168.32.114 | GPU host, Rack #3
cosmic-gpu-5 | 7c:c2:55:14:f0:3a | 192.168.32.115 | GPU host, Rack #3
cosmic-gpu-6 | 3c:ec:ef:f2:1c:50 | 192.168.32.116 | GPU host, Rack #4
cosmic-gpu-7 | 7c:c2:55:14:f0:2a | 192.168.32.117 | GPU host, Rack #4
cosmic-gpu-8 | 3c:ec:ef:f2:fd:12 | 192.168.32.118 | GPU host, Rack #4
cosmic-gpu-9 | 7c:c2:55:14:f0:1a | 192.168.32.119 | GPU host, Rack #4
cosmic-gpu-10 | 7c:c2:55:14:ee:7a | 192.168.32.120 | GPU host, Rack #5
cosmic-gpu-11 | 3c:ec:ef:f1:90:c2 | 192.168.32.121 | GPU host, Rack #5
cosmic-gpu-12 | 7c:c2:55:29:f6:68 | 192.168.32.122 | GPU host, Rack #5
cosmic-gpu-13 | 3c:ec:ef:f3:7f:ea | 192.168.32.123 | GPU host, Rack #5
cosmic-gpu-14 | 7c:c2:55:14:ee:96 | 192.168.32.124 | GPU host, Rack #6
cosmic-gpu-15 | 3c:ec:ef:f3:7e:64 | 192.168.32.125 | GPU host, Rack #6
cosmic-gpu-16 | 3c:ec:ef:f3:7f:f6 | 192.168.32.126 | GPU host, Rack #6
cosmic-gpu-17 | 7c:c2:55:14:ef:7c | 192.168.32.127 | GPU host, Rack #6
cosmic-1g-switch-0 | 10:4f:58:bd:6c:e0 | 192.168.33.30 | 1 GbE switch, SETI Rack #1
cosmic-1g-switch-1 | 10:4f:58:bd:4c:e0 | 192.168.33.31 | 1 GbE switch, SETI Rack #2
cosmic-1g-switch-2 | 9c:a2:f4:75:d9:cf | 192.168.33.32 | 1 GbE switch, SETI Rack #3
cosmic-1g-switch-3 | 1c:61:b4:19:38:ba | 192.168.33.33 | 1 GbE switch, SETI Rack #4
cosmic-1g-switch-4 | 1c:61:b4:19:3d:0c | 192.168.33.34 | 1 GbE switch, SETI Rack #5
cosmic-1g-switch-5 | 1c:61:b4:19:38:b8 | 192.168.33.35 | 1 GbE switch, SETI Rack #6
cosmic-1g-switch-6 | TBC | 192.168.33.36 | 1 GbE switch, SETI Rack #7, Note 1
cosmic-1g-switch-7 | TBC | 192.168.33.37 | 1 GbE switch, SETI Rack #8, Note 1
cosmic-1g-switch-8 | TBC | 192.168.33.38 | 1 GbE switch, SETI Rack #9, Note 1
cosmic-1g-switch-9 | TBC | 192.168.33.39 | 1 GbE switch, SETI Rack #10, Note 1
cosmic-fpga-0-ipmi | a0:42:3f:3f:6f:90 | 192.168.33.100 | FPGA host server IPMI, Rack #1
cosmic-fpga-1-ipmi | a0:42:3f:3f:6f:b4 | 192.168.33.101 | FPGA host server IPMI, Rack #1
cosmic-fpga-2-ipmi | a0:42:3f:3d:2b:26 | 192.168.33.102 | FPGA host server IPMI, Rack #1
cosmic-storage-1-ipmi | 3c:ec:ef:91:63:e3 | 192.168.33.105 | Storage server IPMI, Rack #2
cosmic-storage-2-ipmi | 3c:ec:ef:91:51:d9 | 192.168.33.106 | Storage server IPMI, Rack #2
cosmic-gpu-0-ipmi | 3c:ec:ef:2f:0b:08 | 192.168.33.110 | GPU host IPMI, Rack #2
cosmic-gpu-1-ipmi | 04:42:1a:1b:0b:94 | 192.168.33.111 | GPU host IPMI, Rack #2
cosmic-gpu-2-ipmi | 3c:ec:ef:33:09:00 | 192.168.33.112 | GPU host IPMI, Rack #3
cosmic-gpu-3-ipmi | 3c:ec:ef:33:02:36 | 192.168.33.113 | GPU host IPMI, Rack #3
cosmic-gpu-4-ipmi | 3c:ec:ef:33:02:9b | 192.168.33.114 | GPU host IPMI, Rack #3
cosmic-gpu-5-ipmi | 3c:ec:ef:2f:b1:1b | 192.168.33.115 | GPU host IPMI, Rack #3
cosmic-gpu-6-ipmi | 3c:ec:ef:33:0e:5d | 192.168.33.116 | GPU host IPMI, Rack #4
cosmic-gpu-7-ipmi | 3c:ec:ef:33:03:38 | 192.168.33.117 | GPU host IPMI, Rack #4
cosmic-gpu-8-ipmi | 3c:ec:ef:33:08:ad | 192.168.33.118 | GPU host IPMI, Rack #4
cosmic-gpu-9-ipmi | 3c:ec:ef:33:03:3c | 192.168.33.119 | GPU host IPMI, Rack #4
cosmic-gpu-10-ipmi | 3c:ec:ef:33:0d:9c | 192.168.33.120 | GPU host IPMI, Rack #5
cosmic-gpu-11-ipmi | 3c:ec:ef:33:0e:25 | 192.168.33.121 | GPU host IPMI, Rack #5
cosmic-gpu-12-ipmi | 3c:ec:ef:33:0e:5a | 192.168.33.122 | GPU host IPMI, Rack #5
cosmic-gpu-13-ipmi | 3c:ec:ef:33:0e:64 | 192.168.33.123 | GPU host IPMI, Rack #5
cosmic-gpu-14-ipmi | 3c:ec:ef:ac:81:29 | 192.168.33.124 | GPU host IPMI, Rack #6
cosmic-gpu-15-ipmi | 3c:ec:ef:33:0e:67 | 192.168.33.125 | GPU host IPMI, Rack #6
cosmic-gpu-16-ipmi | 3c:ec:ef:33:0e:26 | 192.168.33.126 | GPU host IPMI, Rack #6
cosmic-gpu-17-ipmi | 3c:ec:ef:33:03:48 | 192.168.33.127 | GPU host IPMI, Rack #6

Note 1: Not yet installed  

### COSMIC 100G Domains (192.168.64.0/23)

Number of hosts anticipated: 256 Compute + "a few" storage / axiliary

#### GPU nodes port (mostly) enp52s0f0np0 (192.168.64.0/24)

Number of hosts anticipated: 128 Compute + "a few" storage / axiliary

This network uses `cosmic-100g-switch-0`.

Host | MAC | IP | Notes
-|-|-|-
cosmic-storage-1-100g-0 | b8:ce:f6:a6:42:81 | 192.168.64.11 | cosmic-storage-1/enp175s0f1np1 (eth3)
cosmic-storage-2-100g-0 | b8:ce:f6:d2:89:6b | 192.168.64.12 | cosmic-storage-2/enp175s0f1np1 (eth3)
cosmic-gpu-0-100g-0 | b8:ce:f6:a6:42:a1 | 192.168.64.100 | cosmic-gpu-0/enp97s0f1
cosmic-gpu-1-100g-0 | 10:70:fd:18:77:cc | 192.168.64.101 | cosmic-gpu-1/enp194s0f0np0 (eth2)
cosmic-gpu-2-100g-0 | b8:3f:d2:13:03:da | 192.168.64.102 | cosmic-gpu-2/enp52s0f0np0 (eth2)
cosmic-gpu-3-100g-0 | b8:3f:d2:13:08:76 | 192.168.64.103 | cosmic-gpu-3/enp52s0f0np0 (eth2)
cosmic-gpu-4-100g-0 | b8:3f:d2:13:06:92 | 192.168.64.104 | cosmic-gpu-4/enp52s0f0np0 (eth2)
cosmic-gpu-5-100g-0 | b8:3f:d2:32:37:fe | 192.168.64.105 | cosmic-gpu-5/enp55s0f0np0 (eth2); Inexplicably different interface name
cosmic-gpu-6-100g-0 | b8:3f:d2:13:4b:2a | 192.168.64.106 | cosmic-gpu-6/enp52s0f0np0 (eth2)
cosmic-gpu-7-100g-0 | b8:3f:d2:13:05:d6 | 192.168.64.107 | cosmic-gpu-7/enp52s0f0np0 (eth2)
cosmic-gpu-8-100g-0 | b8:3f:d2:13:08:5e | 192.168.64.108 | cosmic-gpu-8/enp52s0f0np0 (eth2)
cosmic-gpu-9-100g-0 | b8:3f:d2:13:08:6e | 192.168.64.109 | cosmic-gpu-9/enp52s0f0np0 (eth2)
cosmic-gpu-10-100g-0 | b8:3f:d2:13:09:7a | 192.168.64.110 | cosmic-gpu-10/enp52s0f0np0 (eth2)
cosmic-gpu-11-100g-0 | b8:3f:d2:13:05:72 | 192.168.64.111 | cosmic-gpu-11/enp52s0f0np0 (eth2)
cosmic-gpu-12-100g-0 | b8:3f:d2:13:4a:9a | 192.168.64.112 | cosmic-gpu-12/enp52s0f0np0 (eth2)
cosmic-gpu-13-100g-0 | b8:3f:d2:13:03:d2 | 192.168.64.113 | cosmic-gpu-13/enp52s0f0np0 (eth2)
cosmic-gpu-14-100g-0 | b8:3f:d2:13:0c:ca | 192.168.64.114 | cosmic-gpu-14/enp52s0f0np0 (eth2)
cosmic-gpu-15-100g-0 | b8:3f:d2:13:08:8a | 192.168.64.115 | cosmic-gpu-15/enp52s0f0np0 (eth2)
cosmic-gpu-16-100g-0 | b8:3f:d2:13:06:e2 | 192.168.64.116 | cosmic-gpu-16/enp52s0f0np0 (eth2)
cosmic-gpu-17-100g-0 | b8:3f:d2:13:03:2a | 192.168.64.117 | cosmic-gpu-17/enp52s0f0np0 (eth2)

#### GPU nodes port (mostly) enp225s0f0np0 (192.168.65.0/24)

This network uses `cosmic-100g-switch-1`.

Number of hosts anticipated: 128 Compute + "a few" storage / axiliary

Host | MAC | IP | Notes
-|-|-|-
cosmic-storage-1-100g-1 | b8:ce:f6:a6:42:80 | 192.168.65.11 | cosmic-storage-1/enp175s0f0np0 (eth2)
cosmic-storage-2-100g-1 | b8:ce:f6:d2:89:6a | 192.168.65.12 | cosmic-storage-2/enp175s0f0np0 (eth2)
cosmic-gpu-0-100g-1 | b8:ce:f6:a6:41:89 | 192.168.65.100 | cosmic-gpu-0/enp225s0f1; Uses switch `cosmic-100g-switch-0`
cosmic-gpu-1-100g-1 | 10:70:fd:18:77:cd | 192.168.65.101 | cosmic-gpu-1/enp194s0f1np1 (eth3); Uses switch `cosmic-100g-switch-0`
cosmic-gpu-2-100g-1 | b8:3f:d2:13:07:16 | 192.168.65.102 | cosmic-gpu-2/enp225s0f0np0 (eth4)
cosmic-gpu-3-100g-1 | b8:3f:d2:13:08:26 | 192.168.65.103 | cosmic-gpu-3/enp225s0f0np0 (eth4)
cosmic-gpu-4-100g-1 | b8:3f:d2:13:0b:c2 | 192.168.65.104 | cosmic-gpu-4/enp225s0f0np0 (eth4)
cosmic-gpu-5-100g-1 | b8:3f:d2:13:04:12 | 192.168.65.105 | cosmic-gpu-5/enp225s0f0np0 (eth4)
cosmic-gpu-6-100g-1 | b8:3f:d2:32:37:f6 | 192.168.65.106 | cosmic-gpu-6/enp225s0f0np0 (eth4)
cosmic-gpu-7-100g-1 | b8:3f:d2:13:03:b6 | 192.168.65.107 | cosmic-gpu-7/enp225s0f0np0 (eth4)
cosmic-gpu-8-100g-1 | b8:3f:d2:13:0d:6a | 192.168.65.108 | cosmic-gpu-8/enp225s0f0np0 (eth4)
cosmic-gpu-9-100g-1 | b8:3f:d2:32:37:fa | 192.168.65.109 | cosmic-gpu-9/enp225s0f0np0 (eth4)
cosmic-gpu-10-100g-1 | b8:3f:d2:13:0c:8a | 192.168.65.110 | cosmic-gpu-10/enp225s0f0np0 (eth4)
cosmic-gpu-11-100g-1 | b8:3f:d2:13:07:9a | 192.168.65.111 | cosmic-gpu-11/enp225s0f0np0 (eth4)
cosmic-gpu-12-100g-1 | b8:3f:d2:32:38:02 | 192.168.65.112 | cosmic-gpu-12/enp225s0f0np0 (eth4)
cosmic-gpu-13-100g-1 | b8:3f:d2:13:08:6a | 192.168.65.113 | cosmic-gpu-13/enp225s0f0np0 (eth4)
cosmic-gpu-14-100g-1 | b8:3f:d2:13:0d:76 | 192.168.65.114 | cosmic-gpu-14/enp225s0f0np0 (eth4)
cosmic-gpu-15-100g-1 | b8:3f:d2:13:08:2e | 192.168.65.115 | cosmic-gpu-15/enp225s0f0np0 (eth4)
cosmic-gpu-16-100g-1 | b8:3f:d2:13:07:1a | 192.168.65.116 | cosmic-gpu-16/enp225s0f0np0 (eth4)
cosmic-gpu-17-100g-1 | b8:3f:d2:13:07:b2 | 192.168.65.117 | cosmic-gpu-17/enp225s0f0np0 (eth4)
