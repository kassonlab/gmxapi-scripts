# gmxapi-scripts

Sample scripts for running some high-level tasks including ensemble simulation in gmxapi.

### As of 2022, we recommend using https://github.com/kassonlab/gmxapi-tutorials as the entry point for learning and demonstrating gmxapi.

These scripts demonstrate 2019 and planned functionality under subtasks of 
GROMACS issue [2045](https://redmine.gromacs.org/issues/2045)
and as outlined in the 
[roadmap](https://redmine.gromacs.org/projects/gromacs/repository/revisions/master/entry/python_packaging/roadmap.rst)

The general syntax for the gmxapi user interface in GROMACS 2020 will be finalized by about May 1, 2019.
Please note feedback, questions, and concerns in the [Issues](https://github.com/kassonlab/gmxapi-scripts/issues)
or to issues@gmxapi.org.

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
