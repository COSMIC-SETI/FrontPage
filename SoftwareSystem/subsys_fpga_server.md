# F-Engine Servers

The F-Engines are implemented on FPGAs hosted on servers (`cosmic-fpga-*`).

Programmatic control and access to the F-Engines is exposed via a RESTful endpoint on each server, interaction with which is programmatically wrapped up under the `CosmicFengine` [class](https://github.com/realtimeradio/vla-dev/blob/master/software/control_sw/src/cosmic_fengine.py#L46) of the `cosmic_f_remote` [package](https://github.com/realtimeradio/vla-dev/blob/master/software/control_remote_sw/src/cosmic_fengine.py#L64): the `cosmic-head` node uses the remote simulacra-class to emulate local access of the remotely hosted python instances.

The RESTful endpoints are served under the `remoteobjects_server` systemd service on each of the servers.

Related FAQs:

- [Remapping Antenna to F-Engines](../Memos/faqs.md#remapping-antenna-to-f-engines)
