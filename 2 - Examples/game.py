import numpy as np

WHITE = -1
EMPTY = 0
BLACK = 1

BOARD_SIZE = 3
BOARD_SHAPE = (BOARD_SIZE, BOARD_SIZE)

class GameState:
    def __init__(self):
        self.board = np.full(BOARD_SHAPE, EMPTY)

        self.current = BLACK
        self.is_end = False

    def is_on_board(self, action):
        x, y = action
        return (x >= 0 and x < BOARD_SIZE) and (y >= 0 and y < BOARD_SIZE)

    def is_valid(self, action):
        x, y = action

        return self.is_on_board(action) and self.board[x, y] == EMPTY

    def get_valid_moves(self):
        return list(filter(lambda act: self.is_valid(act),
            [(x, y) for x in range(BOARD_SIZE) for y in range(BOARD_SIZE)]))

    def play(self, action):
        assert not self.is_end
        assert self.is_valid(action)

        x, y = action
        self.board[x, y] = self.current

        self.current = -self.current

    def print_board(self):
        print('   ', end='')
        print('ABCDEFGHJKLMNOPQRSTUVWXYZ'[:BOARD_SIZE], end='')

        for y in range(BOARD_SIZE):
            print()
            print('%2d' % (y+1), end=' ')

            for x in range(BOARD_SIZE):
                if self.board[x, y] == BLACK:
                    print('X', end='')
                elif self.board[x, y] == WHITE:
                    print('O', end='')
                else:
                    print(' ', end='')

        print('   {} to play'.format('B' if self.current == BLACK else 'W'))
