"""
Runner for adaptive MSMs
"""

import gmx
import analysis

# Add a TPR-loading operation to the default work graph (initially empty) that
# produces simulation input data bundle (parameters, structure, topology)

N = 50  # Number of ensemble members
starting_structure = 'input_conf.gro' # Could start with a list of distinct confs
topology_file = 'input.top'
run_parameters = 'params.mdp'

initial_tpr = gmx.commandline_operation('gmx', 'grompp',
                                        input={'-f': run_parameters,
                                        '-p': topology_file,
                                        '-c': starting_structure})
initial_input = gmx.load_tpr([initial_tpr] * N)  # An array of simulations

# We will need a pdb for MSM building in PyEmma
editconf = gmx.commandline_operation('gmx', 'editconf',
    inputs={'-f': starting_structure}
    output={'-o': gmx.OutputFile('.pdb')})  # 'input_conf.pdb'

# Get a placeholder object that can serve as a sub context / work graph owner
# and can be used in a control operation.
subgraph = gmx.subgraph(variables={
                            'conformation': initial_input,
                            'P': [[0.]*N]*N
                            })

with subgraph:
    modified_input = gmx.modify_input(
        input=initial_input, structure=subgraph.conformation)
    md = gmx.mdrun(input=modified_input)
    # Get the output trajectories and pass to PyEmma to build the MSM
    # Return a stop condition object that can be used in gmx while loop to
    # terminate the simulation
    allframes = gmx.commandline_operation('gmx', 'trajcat',
                                          input={'-f': gmx.gather(md.output.trajectory.file)},
                                          output={'-o': gmx.OutputFile('.trr')})

    adaptive_msm = analysis.msm_analyzer(topfile=editconf.file['-o'],
        trajectory=allframes.output.file['-o']
        P=subgraph.P)
    # Update the persistent data for the subgraph
    subgraph.P = adaptive_msm.output.transition_matrix
    # adaptive_msm here is responsible for maintaining the ensemble width
    subgraph.conformation = adaptive_msm.output.conformation

# In the default work graph, add a node that depends on `condition` and
# wraps subgraph.
my_loop = gmx.while_loop(gmx.logical_not(subgraph.adaptive_msm.output.is_converged), subgraph)

gmx.run()
