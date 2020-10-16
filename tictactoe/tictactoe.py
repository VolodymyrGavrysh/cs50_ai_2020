"""
Tic Tac Toe Player
"""
import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    x_count = 0
    o_count = 0

    for i in board:

        x_count += i.count('X')
        o_count += i.count('O')

    if x_count == o_count:
        return X
    else:
        return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    num = set()
    for i in range(0, 3):
        for j in range(0, 3):
            if board[i][j] == EMPTY:
                num.add((i, j))
    return num

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    num = copy.deepcopy(board)
    num[action[0]][action[1]] = player(board)
    return num


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # diagonal 
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        return O
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        return X
    if board[0][2] == O and board[1][1] == O and board[2][0] == O:
        return O
    if board[0][2] == X and board[1][1] == X and board[2][0] == X:
        return X
    # Vertical
    if board[0][0] == O and board[0][1] == O and board[0][2] == O:
        return O
    if board[0][0] == X and board[0][1] == X and board[0][2] == X:
        return X
    if board[1][0] == O and board[1][1] == O and board[1][2] == O:
        return O
    if board[1][0] == X and board[1][1] == X and board[1][2] == X:
        return X
    if board[2][0] == O and board[2][1] == O and board[2][2] == O:
        return O
    if board[2][0] == X and board[2][1] == X and board[2][2] == X:
        return X
    # horisontal
    if board[0][0] == O and board[1][0] == O and board[2][0] == O:
        return O
    if board[0][0] == X and board[1][0] == X and board[2][0] == X:
        return X
    if board[0][1] == O and board[1][1] == O and board[2][1] == O:
        return O
    if board[0][1] == X and board[1][1] == X and board[2][1] == X:
        return X
    if board[0][2] == O and board[1][2] == O and board[2][2] == O:
        return O
    if board[0][2] == X and board[1][2] == X and board[2][2] == X:
        return X

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # terminal = False
    # num = 0
    # for i in board:
    #     num += i.count(EMPTY)
    # if winner(board) is not None and num == 0:
    #     terminal = True
    # return terminal
    if winner(board) is not None or (not any(EMPTY in sublist for sublist in board) and winner(board) is None):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    playing = player(board)
    
    if playing == X:
        v = -math.inf
        for action in actions(board):
            move = min_value(result(board, action))
            if move > v:
                v = move
                best_move = action
    else:
        v = math.inf 
        for action in actions(board):
            move = max_value(result(board, action))
            if move < v:
                v = move
                best_move = action
    return best_move

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, max_value(result(board, action)))
    return v

def min_value(board):   
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v