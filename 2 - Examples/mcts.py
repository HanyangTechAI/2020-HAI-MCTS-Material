import numpy as np


class TreeNode:
    '''
    each node have some information and statistics.

    action : action of node
    color : color of node
    parent : parent node
    children : list of children

    N : the number of visits
    W : the sum of values
    P : policy value
    '''
    def __init__(self, action, color, parent: TreeNode, prior: float):
        pass

    '''
    select node with argmax(Q + u)
    '''
    def select(self) -> TreeNode:
        pass

    '''
    expend this node
    '''
    def expand(self, state, policy: np.array):
        pass

    '''
    update statistics of node
    '''
    def update(self, value: float):
        pass


class MCTSEngine:
    '''
    initialize root node
    '''
    def __init__(self):
        pass

    '''
    generate best move after simulations
    '''
    def genmove(self, n_simulations: int):
        pass
