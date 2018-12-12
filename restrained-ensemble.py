#!/usr/bin/env python
"""Run restrained-ensemble sampling and biasing workflow.

Irrgang, M. E., Hays, J. M., & Kasson, P. M.
gmxapi: a high-level interface for advanced control and extension of molecular dynamics simulations.
*Bioinformatics* 2018.
DOI: `10.1093/bioinformatics/bty484 <https://doi.org/10.1093/bioinformatics/bty484>`_
"""

# Restrained-ensemble formalism is a variant of that defined by Roux et al., 2013

import os
import sys

import gmx
import myplugin

# The user has already built 20 input files in 20 directories.
size = 20
input_dir_list = ['aa_{:02d}'.format(i) for i in range(size)]
tpr_list = [os.path.abspath(os.path.join(directory, 'mRMR.tpr')) for directory in input_dir_list]

restraint1_params = 'params1.json'
restraint2_params = 'params2.json'

potential1 = myplugin.ensemble_restraint('ensemble_restraint_1', params=restraint1_params)
potential2 = myplugin.ensemble_restraint('ensemble_restraint_2', params=restraint2_params)

md = gmx.mdrun(gmx.read_tpr(tpr_list))
md.interface.potential.add(potential1)
md.interface.potential.add(potential2)

# Settings for a 20 core HPC node. Use 18 threads for domain decomposition for pair potentials
# and the remaining 2 threads for PME electrostatics.
gmx.run(md, tmpi=20, grid=[3, 3, 2], ntomp_pme=1, npme=2, ntomp=1)
