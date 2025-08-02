# Software System Troubleshooting

## Commensal Observation Failures

Captured below are failures reported by the [observation control sub-system](./subsys_observation_control.md) to observe commensally. The errors are typically noted in the `active_vla_observations` Slack channel, with fuller tracebacks provided in the logs.

### Configuration Failed: CosmicFengine has no attribute 'eths'

<details>
<summary>
`RemoteObjectError("Error calling an object's method: pcie64_0.disable_tx({})", "'CosmicFengine' object has no attribute 'eths'"...`
</summary>

```
Traceback (most recent call last):
  File "../COSMIC-VLA-PythonLibs/scripts/observe.py", line 257, in <module>
    raise err
  File "../COSMIC-VLA-PythonLibs/scripts/observe.py", line 223, in <module>
    antarray_config, _ = observation_marshall.configure_observation(
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/site-packages/cosmic/observations/marshall.py", line 390, in configure_observation
    self.thread_pool.map(lambda feng: feng.disable_tx(), ant_feng_dict.values())
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/multiprocessing/pool.py", line 364, in map
    return self._map_async(func, iterable, mapstar, chunksize).get()
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/multiprocessing/pool.py", line 771, in get
    raise self._value
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/multiprocessing/pool.py", line 125, in worker
    result = (True, func(*args, **kwds))
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/multiprocessing/pool.py", line 48, in mapstar
    return list(map(*args))
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/site-packages/cosmic/observations/marshall.py", line 390, in <lambda>
    self.thread_pool.map(lambda feng: feng.disable_tx(), ant_feng_dict.values())
  File "<string>", line 4, in disable_tx
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/site-packages/remoteobjects/client/rest_client.py", line 54, in _post
    return self._manage_CRUD_request(requests.post, endpoint, data, params, files)
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/site-packages/remoteobjects/client/remote_instance.py", line 60, in _manage_CRUD_request
    return super()._manage_CRUD_request(
  File "/home/cosmic/anaconda3/envs/cosmic_vla/lib/python3.8/site-packages/remoteobjects/client/remote_object.py", line 104, in _manage_CRUD_request
    raise RemoteObjectError(
remoteobjects.client.remote_object.RemoteObjectError: 
Remote Traceback:
Traceback (most recent call last):
  File "/home/cosmic/py3-venv/lib/python3.8/site-packages/remoteobjects/server/endpoints.py", line 289, in post
    "return": __REMOTE_OBJECT_REGISTRY__.obj_call_method(
  File "/home/cosmic/py3-venv/lib/python3.8/site-packages/remoteobjects/server/object_registry.py", line 195, in obj_call_method
    return self._obj_call_method(obj, method_name, method_args_dict)
  File "/home/cosmic/py3-venv/lib/python3.8/site-packages/remoteobjects/server/object_registry.py", line 122, in _obj_call_method
    return func(**method_args_dict)
  File "/home/cosmic/py3-venv/lib/python3.8/site-packages/cosmic_f/cosmic_fengine.py", line 1856, in disable_tx
    for i, eth in enumerate(self.eths):
AttributeError: 'CosmicFengine' object has no attribute 'eths'
Error calling an object's method: `pcie64_0.disable_tx({})`
```

</details>

The FPGA's have not been programmed with any reasonable firmware and so accessing the 'register' tied member field `eths` results in an error.

*Solution:*

Restart the FPGA services which will flash a fundamental firmware to the FPGAs. 
`ansible-playbook ~cosmic/dev/FrontPage/Nodes/Head/ansible_playbooks/fpga_service_restart.yml`