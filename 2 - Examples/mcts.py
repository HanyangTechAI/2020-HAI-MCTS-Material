import copy
import numpy as np
import math

import game


C_PUCT = 0.8

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
    def __init__(self, action, color, parent, prior: float):
        self.action = action
        self.color = color
        self.parent = parent
        self.children = []

        self.N = 0
        self.W = 0
        self.P = prior

    '''
    return whether this node is leaf
    '''
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    '''
    select node with argmax(Q + u)
    '''
    def select(self):
        # 1. Q, u값을 계산
        # 2. Q+u 가장 큰 node를 반환

        # Q+u 더한것을 저장하는 array
        values = np.zeros(len(self.children))

        for i, child in enumerate(self.children):
            Q = child.W / child.N if child.N != 0 else 0
            u = C_PUCT * child.P * math.sqrt(self.N) / (1 + child.N)

            values[i] = Q + u

        return self.children[np.argmax(values)]

    '''
    expend this node
    '''
    def expand(self, state, policy: np.array):
        # 1. 가능한 모든 수 list
        # 2. list에 대한 policy로 node를 생성

        for pt in state.get_valid_moves():
            x, y = pt
            idx = x + y * game.BOARD_SIZE

            self.children.append(TreeNode(pt, state.current, self, policy[idx]))

    '''
    update statistics of node
    '''
    def update(self, value: float):
        self.N += 1
        self.W += value


class MCTSEngine:
    '''
    initialize root node
    '''
    def __init__(self):
        self.state = game.GameState()
        self.root = TreeNode(None, -self.state.current, None, 0)

    '''
    generate best move after simulations
    '''
    def genmove(self, n_simulations: int):
        for simul in range(n_simulations):
            state = copy.deepcopy(self.state)

            # selection
            current = self.root
            while not current.is_leaf():
                current = current.select()
                state.play(current.action)

            # now current is leaf node

            # p(a|s)
            policy = np.random.rand(game.BOARD_SIZE ** 2)
            policy /= np.sum(policy)

            value = np.random.uniform(low=-1, high=1, size=(1, )).item()

            # expand
            current.expand(state, policy)

            # backpropagation
            while current.parent != None:
                update_value = value if current.color == state.current else -value

                current.update(update_value)
                current = current.parent

        # play policy (the highest visits)
        max_child = None
        max_value = -999

        for child in self.root.children:
            if child.N > max_value:
                max_child = child
                max_value = child.N

        return max_child.action

    '''
    print search result
    '''
    def dump_stat(self):
        for child in self.root.children:
            print('action {} - policy: {:.2f} value: {:.2f} visits: {}'.format(
                child.action, child.P, child.W/child.N if child.N != 0 else 0, child.N
            ))
