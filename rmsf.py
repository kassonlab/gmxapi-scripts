import gmx

# Add a TPR-loading operation to the default work graph (initially empty) that
# produces simulation input data bundle (parameters, structure, topology)

# Make N run input files
N = 50  # Number of ensemble members
starting_structure = 'input_conf.gro'
topology_file = 'input.top'
run_parameters = 'params.mdp'

initial_tpr = gmx.OutputFile('.tpr')
gmx.commandline_operation('gmx', 'grompp',
                          input={'-f': run_parameters,
                                 '-c': starting_structure,
                                 '-p': topology_file},
                          output={'-o': initial_tpr}
                          )
# Note: Before gmx.OutputFile, users still have to manage filenames
# The above would have `output={'-o': [initial_tpr] * N}`

# Note: initial_tpr has a single output that can be automatically broadcast now or later.
# Broadcast to the read_tpr operation:
#simulation_input = gmx.read_tpr([initial_tpr] * N)
# Wait to broadcast until the next operation:
simulation_input = gmx.read_tpr(initial_tpr)

# Array inputs imply array outputs.
input_array = gmx.modify_input(simulation_input,
                               params={'taut-t': list(range(50)) / 10.0}
                               )

md = gmx.mdrun(input_array)  # An array of simulations

xvg_data = gmx.OutputFile('.xvg')
rmsf = gmx.commandline_operation('gmx', 'rmsf',
                                 input={'-f': md.output.trajectory,
                                        '-s': initial_tpr
                                        },
                                 output={'-o': xvg_data}
                                 )
output_files = gmx.gather(xvg_data.filename)
gmx.run()

print('Output file list:')
print(', '.join(output_files.extract())
