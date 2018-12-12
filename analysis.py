"""
Analysis tool for adaptive msms
"""

import gmx
import pyemma
import pyemma.coor as coor

def relative_entropy(P, Q):
    """
    Takes two transition matrices, calculates relative entropy
    """
    return rel_entropy_P_Q

class MSMAnalyzer:
    """
    Builds msm from gmxapi output trajectory
    """
    def __init__(self, topfile, trajectory, P):
        feat = coor.featurizer(topfile)
        X = coor.load(trajectory, feat)
        Y = coor.tica(X, dim=2).get_output()
        self.k_means = coor.cluster_kmeans(Y)
        self.Q = P
        self.P = new_msm_transition_matrix
    def is_converged(self):
        # Q = n-1 transition matrix, P = n transition matrix
        Q = self.Q
        return (relative_entropy(self.P, self.Q) < tol)
    def transition_matrix(self):
        return self.P

msm_analyzer = gmx.operation.make_operation(MSMAnalyzer,
input=['topfile', 'trajectory', 'P'],
output=['is_converged', 'transition_matrix']
)
