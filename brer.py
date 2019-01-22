"""
New DEER incorporation workflow in gmxapi
"""

import json

import gmx
import myplugin  # Custom potentials
import brer_tools

# Add a TPR-loading operation to the default work graph (initially empty) that
# produces simulation input data bundle (parameters, structure, topology)

N = 50  # Number of ensemble members
starting_structure = 'input_conf.gro'  # Could start with a list of distinct tprs
topology_file = 'input.top'
run_parameters = 'params.mdp'
potential_parameters = 'myparams.json'
with open(potential_parameters, mode='r') as fh:
    my_dict_params = json.load(fh)

# make a single simulation input file
initial_tpr = gmx.commandline_operation(
    'gmx',
    'grompp',
    input={
        '-f': run_parameters,
        '-p': topology_file,
        '-c': starting_structure
    })
initial_input = gmx.load_tpr(gmx.MDArray(initial_tpr, N))  # An array of simulations

# just to demonstrate gmxapi functionality, modify a parameter here
# changed parameters with width 1 on an ensemble with width 50
# if we wanted each ensemble member to have a different value, we would just
# have the new parameter value be an array of width 50
lengthened_input = gmx.modify_input(
    initial_input, parameters={'nsteps': 50000000})

# Create subgraph objects that encapsulate multiple operations
# and can be used in conditional and loop operations.
# For subgraphs, inputs can be accessed as variables (not standard input/output)
# and are copied to the next iteration.
train = gmx.subgraph(variables={'conformation': initial_input})

with train:
    training_potential = myplugin.training_restraint(
        'training_restraint', params=my_dict_params)
    modified_input = gmx.modify_input(
        input=initial_input, structure=train.conformation)
    md = gmx.mdrun(input=modified_input, potential=training_potential)
    # Alternate syntax to facilitate adding multiple potentials:
    # md.interface.potential.apend(training_potential)
    train_condition = brer_tools.training_analyzer(
        training_potential.output.alpha)
    train.conformation = md.output.conformation

# In the default work graph, add a node that depends on `condition` and
# wraps subgraph.
train_loop = gmx.while_loop(
    gmx.logical_not(train.train_condition.is_converged), train)

# in this particular application, we "roll back" to the initial input
converge = gmx.subgraph(variables={'conformation': initial_input})

with converge:
    modified_input = gmx.modify_input(
        input=initial_input, structure=converge.conformation)
    converging_potential = myplugin.converge_restraint(
        params=training_potential.output)
    converge_condition = brer_tools.converge_analyzer(
        converging_potential.output.distances)
    md = gmx.mdrun(input=modified_input, potential=converging_potential)
conv_loop = gmx.while_loop(
    gmx.logical_not(converge.converge_condition.is_converged), converge)

production_input = gmx.modify_input(
    input=initial_input, structure=converge.conformation)
prod_potential = myplugin.production_restraint(
    params=converging_potential.output)
prod_md = gmx.mdrun(input=production_input, potential=prod_potential)

gmx.run()

print('Final alpha value was {}'.format(
    training_potential.output.alpha.extract()))
# also can extract conformation filenames, etc.
