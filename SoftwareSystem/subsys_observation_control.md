# Overview

The time on the VLA instrument is divided into 'scans'. A COSMIC 'observation' is the demarcation of a scan towards a desired recording of 1 or more files.

# VLA scans

The meta-data of the VLA scans are [captured from MCAST](https://github.com/demorest/evla_mcast/blob/41365b1cce32e244cd3469fc3fc2cb3b3949b1e5/evla_mcast/mcast_clients.py#L80-L118) publications. This scan meta-data populates the `META` redis hash and is also published on the `meta_obs` redis channel.

# COSMIC Observations

Observations have criteria that differentiate them. The criteria are typically against scan meta-data (in the `META` redis hash) but can be measured against the content of any redis hash. When the observation-criteria are met, the configuration of the F and X-Engines is executed. After this configuration, the record-criteria of the observation need to be met before the X-Engines are instructed to "record". Potentially, there is further post-processing of the X-Engines' recorded outputs which is not waited upon by the observation control and so is executed independently.

All the information detailing an observation is laid out in an [observation YAML](https://github.com/COSMIC-SETI/COSMIC-VLA-PythonLibs/blob/main/docs/yaml_schema.md) file, which the observation service seeks to manage the fulfillment of.

# Hashpipe Meta-Marshalling

The data acquisition pipeline is a [hashpipe](./data_acquisition.md#hashpipe) instance.
The hashpipe instances require information about the data-streams that each ingests, in order to correctly achieve collation of the recording's data.

The dimensions of each hashpipe instance's data-stream is deduced by querying the headers of each F-Engines egress packets. That and other meta-data about the observation to be recorded are populated in the key-value based status-buffer of the hashpipe instances.
