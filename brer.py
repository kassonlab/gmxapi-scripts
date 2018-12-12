"""
New DEER incorporation workflow in gmxapi
"""

import gmx
import myplugin  # Custom potential
import analysis


# Add a TPR-loading operation to the default work graph (initially empty) that
# produces simulation input data bundle (parameters, structure, topology)

N = 50  # Number of ensemble members
initial_tpr = 'my_tpr.tpr'  # Could start with a list of distinct tprs
initial_input = gmx.load_tpr([initial_tpr] * N)  # An array of simulations

# Get a placeholder object that can serve as a sub context / work graph owner
# and can be used in a control operation.
train = gmx.subgraph(input={'conformation': initial_input})
converge = gmx.subgraph(input={'conformation'})

with train:
    modified_input = gmx.modify_input(input=initial_input,
    structure=train.input.conformation)
    md = gmx.mdrun(input=initial_input)
    potential = gmx.workflow.WorkElement(
                namespace="myplugin",
                operation="training_restraint",
                depends=[],
                params=my_dict_params)
    potential.name = 'training'
    # you can add multiple restraints by adding work elements

    md.add_dependency(myplugin)
    # is there even going to be a gmx.context? What the heck is the context
    # really though? Why should I be retrieving a potential from it, and how
    # to explain if someone is really intersted in this??
    train_condition = analysis.training_analyzer(gmx.context.potentials['alpha'])

# In the default work graph, add a node that depends on `condition` and
# wraps subgraph.
my_loop = gmx.while_loop(gmx.logical_not(train_condition.is_converged), train)
my_dict_params['alpha'] = gmx.context.potentials['alpha']

with converge:
    # SHould this really be done through subgraphs?? I need the output of
    # one to go to the output of another so maybe, except NOT the output of
    # train -> converge, only converge -> production
    modified_input = gmx.modify_input(input=initial_input,
    structure=train.input.conformation)
    md = gmx.mdrun(input=initial_input)
    potential = gmx.workflow.WorkElement(
                namespace="myplugin",
                operation="converge_restraint",
                depends=[],
                params=my_dict_params)
    converge_condition = analysis.converge_anlayzer(gmx.context.potential.distances)
    # gmx.context.potential.distances seems goofy. Could do commandline?

with production:
    modified_input = gmx.modify_input(input=initial_input,
    structure=converge.output.conformation)
    md = gmx.mdrun(input=initial_input)
    potential = gmx.workflow.WorkElement(
                namespace="myplugin",
                operation="production_restraint",
                depends=[],
                params=my_dict_params)

gmx.run()
