"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None
# X is the maximising player, O is the minimising player


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_moves_taken_X = 0
    num_moves_taken_O = 0

    for row in board:
        for value in row:
            if value == X:
                num_moves_taken_X += 1
            elif value == O:
                num_moves_taken_O += 1

    if num_moves_taken_X == num_moves_taken_O:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    (i = row index, j = column index)
    """
    actions = set()
    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check action is possible
    if not action in actions(board):
        raise ValueError("given action has already been taken")

    moving_player = player(board)

    i, j = action

    new_board = [row[:] for row in board]

    new_board[i][j] = moving_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Returns None if there is no winner.
    """
    # Check Rows
    for row in board:
        if row[0] != EMPTY and row[0] == row[1] == row[2]:
            return row[0]

    # Check Columns
    for j in range(3):
        if board[0][j] != EMPTY and board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]

    # Check Diagonals
    if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # No Winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    # Check if tie
    if all(EMPTY not in row for row in board):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_player = winner(board)
    if winning_player == X:
        return 1
    elif winning_player == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    def max_value(board, alpha=-math.inf, beta=math.inf):
        if terminal(board):
            return utility(board)

        v = -math.inf

        for action in actions(board):
            v = max(v, min_value(result(board, action), alpha, beta))

            alpha = max(alpha, v)
            if alpha >= beta:
                break

        return v

    def min_value(board, alpha=-math.inf, beta=math.inf):
        if terminal(board):
            return utility(board)

        v = math.inf

        for action in actions(board):
            v = min(v, max_value(result(board, action), alpha, beta))

            beta = min(beta, v)
            if alpha >= beta:
                break

        return v

    current_player = player(board)
    best_action = None
    alpha = -math.inf
    beta = math.inf

    if current_player == X:
        best_value = -math.inf
        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, best_value)
    else:
        best_value = math.inf
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            if value < best_value:
                best_value = value
                best_action = action
            beta = min(beta, best_value)


    return best_action
