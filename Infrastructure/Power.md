# COSMIC Power Infrastructure

## Power Distribution Units

Each COSMIC rack is supplied by a single APC APDU9941 Power Distribution Unit.

These PDUs are accessible on the NRAO network under the hostnames `cosmic-pdu-X.vla.nrao.edu`,
where `X` is the zero-indexed COSMIC rack number.
I.e., the PDU in the first COSMIC rack has hostname `cosmic-pdu-0`.

Each PDU is `30 A` derated for `24 A` / `5 kVA`.

Each PDU _bank_ is rated for `16 A`. Exceeding this limit results in a physical breaker tripping, which can only be reset with physical intervention.
Note that there is _no_ ability to definitively detect if the bank circuit breakers have tripped (everything on the PDU user interface will look fine) except by observing zero current draw on the relevant PDU banks.

## PDU Layout

### Rack 1

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
1 | `cosmic-pdu-0` | 1 | 1 | `cosmic-fpga-0` | 
1 | `cosmic-pdu-0` | 2 | 1 | `cosmic-fpga-0` | 
1 | `cosmic-pdu-0` | 3 | 1 | `cosmic-fpga-0` | 
1 | `cosmic-pdu-0` | 4 | 1 | `cosmic-fpga-0` | 
1 | `cosmic-pdu-0` | 5 | 1 | `cosmic-fpga-1` | 
1 | `cosmic-pdu-0` | 6 | 1 | `cosmic-fpga-1` | 
1 | `cosmic-pdu-0` | 7 | 1 | `cosmic-fpga-1` | 
1 | `cosmic-pdu-0` | 9 | 1 | `cosmic-fpga-1` | 
1 | `cosmic-pdu-0` | 10 | 1 | `cosmic-fpga-2` | 
1 | `cosmic-pdu-0` | 11 | 1 | `cosmic-fpga-2` | 
1 | `cosmic-pdu-0` | 12 | 1 | `cosmic-fpga-2` | 
1 | `cosmic-pdu-0` | 13 | 2 | `cosmic-fpga-2` | 
1 | `cosmic-pdu-0` | 17 | 2 | `cosmic-100g-switch-0` | 
1 | `cosmic-pdu-0` | 18 | 2 | `cosmic-100g-switch-0` | 
1 | `cosmic-pdu-0` | 19 | 2 | `cosmic-head` | 
1 | `cosmic-pdu-0` | 20 | 2 | `cosmic-head` | 
1 | `cosmic-pdu-0` | 21 | 2 | `cosmic-100g-switch-1` | 
1 | `cosmic-pdu-0` | 22 | 2 | `cosmic-100g-switch-1` | 
1 | `cosmic-pdu-0` | 23 | 2 | `cosmic-1g-switch-0` | 

### Rack 2

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
2 | `cosmic-pdu-1` | 1 | 1 | `cosmic-gpu-0` | 
2 | `cosmic-pdu-1` | 2 | 1 | `cosmic-gpu-0` | 
2 | `cosmic-pdu-1` | 3 | 1 | `cosmic-gpu-0` | 
2 | `cosmic-pdu-1` | 4 | 1 | `cosmic-gpu-0` | 
2 | `cosmic-pdu-1` | 5 | 1 | `cosmic-gpu-1` | 
2 | `cosmic-pdu-1` | 6 | 1 | `cosmic-gpu-1` | 
2 | `cosmic-pdu-1` | 14 | 2 | `cosmic-storage-1` | 
2 | `cosmic-pdu-1` | 15 | 2 | `cosmic-storage-2` | 
2 | `cosmic-pdu-1` | 23 | 2 | `cosmic-1g-switch-1` | 

### Rack 3

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
3 | `cosmic-pdu-2` | 1 | 1 | `cosmic-gpu-2` | 
3 | `cosmic-pdu-2` | 2 | 1 | `cosmic-gpu-2` | 
3 | `cosmic-pdu-2` | 3 | 1 | `cosmic-gpu-3` | 
3 | `cosmic-pdu-2` | 4 | 1 | `cosmic-gpu-3` | 
3 | `cosmic-pdu-2` | 13 | 2 | `cosmic-gpu-4` | 
3 | `cosmic-pdu-2` | 14 | 2 | `cosmic-gpu-4` | 
3 | `cosmic-pdu-2` | 15 | 2 | `cosmic-gpu-5` | 
3 | `cosmic-pdu-2` | 17 | 2 | `cosmic-gpu-5` | 
3 | `cosmic-pdu-2` | 23 | 2 | `cosmic-1g-switch-2` | 

### Rack 4

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
4 | `cosmic-pdu-3` | 1 | 1 | `cosmic-gpu-6` | 
4 | `cosmic-pdu-3` | 2 | 1 | `cosmic-gpu-6` | 
4 | `cosmic-pdu-3` | 3 | 1 | `cosmic-gpu-7` | 
4 | `cosmic-pdu-3` | 4 | 1 | `cosmic-gpu-7` | 
4 | `cosmic-pdu-3` | 13 | 2 | `cosmic-gpu-8` | 
4 | `cosmic-pdu-3` | 14 | 2 | `cosmic-gpu-8` | 
4 | `cosmic-pdu-3` | 15 | 2 | `cosmic-gpu-9` | 
4 | `cosmic-pdu-3` | 17 | 2 | `cosmic-gpu-9` | 
4 | `cosmic-pdu-3` | 23 | 2 | `cosmic-1g-switch-3` | 

### Rack 5

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
5 | `cosmic-pdu-4` | 1 | 1 | `cosmic-gpu-10` | 
5 | `cosmic-pdu-4` | 2 | 1 | `cosmic-gpu-10` | 
5 | `cosmic-pdu-4` | 3 | 1 | `cosmic-gpu-11` | 
5 | `cosmic-pdu-4` | 4 | 1 | `cosmic-gpu-11` | 
5 | `cosmic-pdu-4` | 13 | 2 | `cosmic-gpu-12` | 
5 | `cosmic-pdu-4` | 14 | 2 | `cosmic-gpu-12` | 
5 | `cosmic-pdu-4` | 15 | 2 | `cosmic-gpu-13` | 
5 | `cosmic-pdu-4` | 17 | 2 | `cosmic-gpu-13` | 
5 | `cosmic-pdu-4` | 23 | 2 | `cosmic-1g-switch-4` | 

### Rack 6

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
6 | `cosmic-pdu-5` | 1 | 1 | `cosmic-gpu-14` | 
6 | `cosmic-pdu-5` | 2 | 1 | `cosmic-gpu-14` | 
6 | `cosmic-pdu-5` | 3 | 1 | `cosmic-gpu-15` | 
6 | `cosmic-pdu-5` | 4 | 1 | `cosmic-gpu-15` | 
6 | `cosmic-pdu-5` | 13 | 2 | `cosmic-gpu-16` | 
6 | `cosmic-pdu-5` | 14 | 2 | `cosmic-gpu-16` | 
6 | `cosmic-pdu-5` | 15 | 2 | `cosmic-gpu-17` | 
6 | `cosmic-pdu-5` | 17 | 2 | `cosmic-gpu-17` | 
6 | `cosmic-pdu-5` | 23 | 2 | `cosmic-1g-switch-5` | 

### Rack 7

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
7 | `cosmic-pdu-6` | 1 | 1 | `cosmic-gpu-18:R1` | 
7 | `cosmic-pdu-6` | 2 | 1 | `cosmic-gpu-18:R2` | 
7 | `cosmic-pdu-6` | 3 | 1 | `cosmic-gpu-18:L1` | 
7 | `cosmic-pdu-6` | 4 | 1 | `cosmic-gpu-18:L2` | 
7 | `cosmic-pdu-6` | 5 | 1 | `cosmic-gpu-19:R1` | 
7 | `cosmic-pdu-6` | 6 | 1 | `cosmic-gpu-19:R2` | 
7 | `cosmic-pdu-6` | 7 | 1 | `cosmic-gpu-19:L1` | 
7 | `cosmic-pdu-6` | 8 | 1 | `cosmic-gpu-19:L2` | 
7 | `cosmic-pdu-6` | 14 | 2 | `cosmic-gpu-20:R1` | 
7 | `cosmic-pdu-6` | 15 | 2 | `cosmic-gpu-20:R2` | 
7 | `cosmic-pdu-6` | 17 | 2 | `cosmic-gpu-20:L1` | 
7 | `cosmic-pdu-6` | 18 | 2 | `cosmic-gpu-20:L2` | 
7 | `cosmic-pdu-6` | 23 | 2 | `cosmic-1g-switch-6` | 

### Rack 8

Rack Number | PDU Hostname | PDU port | PDU bank | Device | Notes
-|-|-|-|-|-
8 | `cosmic-pdu-7` | 1 | 1 | `cosmic-gpu-21:RR` | 
8 | `cosmic-pdu-7` | 2 | 1 | `cosmic-gpu-21:LL` | 
8 | `cosmic-pdu-7` | 3 | 1 | `cosmic-gpu-22:RR` | 
8 | `cosmic-pdu-7` | 4 | 1 | `cosmic-gpu-22:LL` | 
8 | `cosmic-pdu-7` | 13 | 2 | `cosmic-gpu-23:RR` | 
8 | `cosmic-pdu-7` | 14 | 2 | `cosmic-gpu-23:LL` | 
8 | `cosmic-pdu-7` | 23 | 2 | `cosmic-1g-switch-7` | 

### Rack 9

_No hardware installed yet_

### Rack 10

_No hardware installed yet_
