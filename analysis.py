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
    def __init__(self, topfile, trajectory):
        feat = coor.featurizer(topfile)
        X = coord.load(trajectory, feat)
        Y = coord.tica(X, dim=2).get_output()
        self.k_means = coor.cluster_kmeans(Y)
    def is_converged():
        # Question: how do I make P and Q persist in the subgraph? These are
        # transition matrices in the n and n-1 iterations
        return (relative_entropy(P,Q) < tol)

msm_analyzer = gmx.operation.make_operation(MSMAnalyzer, input=['topfile', 'trajectory'])
