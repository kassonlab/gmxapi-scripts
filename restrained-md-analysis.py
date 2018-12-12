import numpy as np


class CalculateJS:
    def __init__(self, params=None, simulation_distances=None):
        """ Do JS-Div calculation """

        _, simulation_histogram = np.histogram(
            simulation_distances, bins=restraint_params['bins'])
        self.js = js_calculation(restraint_params['DEER'],
                                 simulation_histogram)

    def is_converged(self):
        return self.js < tol


calculate_js = gmx.operation.make_operation(
    CalculateJS,
    input=['params', 'simulation_distances'],
    output=['is_converged'])
