# gmxapi-scripts

Sample scripts for running some high-level tasks including ensemble simulation in gmxapi.

These scripts demonstrate current and near-term planned functionality.  
They are not extensively documented yet but are intended to show how the API will enable 
a range of user tasks.

## Examples

### `brer.py`

BRER simulation-analysis protocol implemented as a gmxapi script, with a Python analysis
 module (`brer_tools.py` not implemented here) and C++ MD extension code (`myplugin.so` also not shown).

### `restrained_ensemble.py`

Restrained ensemble example script using restraint potentials implemented in `myplugin` (not shown) and analysis code
 expressed in `restrained_md_analysis.py`.

### `rmsf.py`

Run simulations with a range of `tau-t` values and analyze
with the `gmx rmsf` tool.

### `run_adaptive_msm.py`

Use custom analysis code from `analysis.py` to set the initial conformations for iterations of simulation batches.
