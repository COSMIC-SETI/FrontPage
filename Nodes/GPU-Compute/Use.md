## Offline Correlator (Rawx.jl)

The following support script exists at `/mnt/buf0/beamform_offline/rawxrun_cli.jl`:
```julia
import YAML

using Rawx

cd(@__DIR__)
telinfo = YAML.load_file("/mnt/buf0/beamform_offline/telinfo_vla.yaml", dicttype=Dict{Symbol,Any})
obsinfo = YAML.load_file("/mnt/buf0/beamform_offline/obsinfo.yaml", dicttype=Dict{Symbol,Any})
inttime_per_dump = parse(Float64, ARGS[3])


rawstem = ARGS[1]
uvh5file = ARGS[2]
if isfile(uvh5file)
  @info "removing existing output file $uvh5file"
  rm(uvh5file)
end

# Uses Julia >=1.5 bare keyword argument feature!
Rawx.rawtouvh5(rawstem, uvh5file; telinfo, obsinfo, inttime_per_dump)
```

Exemplary use: `julia --threads 8 ./rawxrun_cli.jl /mnt/buf0/beamform_offline/input/guppi_214410_25779_50352885131_3C84_0001 /mnt/buf0/beamform_offline/guppi_214410_3C84.uvh5 0.016384`

Ensure that the `/mnt/buf0/beamform_offline/obsinfo.yaml` file expresses the observation configuration correctly.

## Rawspec

Rawspec can be used to split the antenna of the input file out into separate filterbank outputs, with the `-S` flag.
See `rawspec -h` for more information.

```
/home/cosmic/src/rawspec/rawspec -S -f 262144 -t 2 -o /mnt/buf0/beamform_offline/ /mnt/buf0/beamform_offline/input/guppi_214410_25779_50352885131_3C84_0001
```