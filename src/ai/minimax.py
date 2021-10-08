import random
from time import time

from src.constant import ShapeConstant
from src.model import State
from src.utility import is_out, is_win, is_full, place
from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def eval(self, state: State):
        return 1  # return format dictionary{move: ("col", "shape"), val: int}}

    def findBlankRow(self, col: int):
        for row in range(state.board.row - 1, -1, -1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                return row

        return -1

    def minimax(self, state: State, n_player: int, thinking_time: float, depth: int, isMax: bool):
        score = eval(state)
        if depth == 0:  # If leaf node
            # return format dictionary{"move": ("col", "shape"), "val": int}}
            return score

        if is_full(state.board):  # If terminal
            # return format dictionary{"move": ("col", "shape"), "val": int}}
            return 0

        if (isMax):  # Maximizer
            best = {"move": ("col", "shape"), "val": -999999}

            # traverse movement
            for i in range(state.board.col):
                for j in range(2):
                    if findBlankRow(i) != -1:
                        if j % 2 == 0:  # Cross Shape
                            if state.players[n_player].quota[ShapeConstant.CROSS] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CROSS, GameConstant.PLAYER_COLOR[n_player])

                                state.board.set_piece(
                                    findBlankRow(i), i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] > best["val"]:
                                    best = alt

                                # Erase Move
                                # xxxxxxxxxx WIP

                        else:  # Circle Shape
                            if state.players[n_player].quota[ShapeConstant.CIRCLE] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CIRCLE, GameConstant.PLAYER_COLOR[n_player])

                                state.board.set_piece(
                                    findBlankRow(i), i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] > best["val"]:
                                    best = alt

                                # Erase Move
                                # xxxxxxxxxx WIP

            return best
        else:  # Minimizer
            best = {move: ("col", "shape"), val: 999999}
            # traverse movement
            for i in range(state.board.col):
                for j in range(2):
                    if findBlankRow(i) != -1:
                        if j % 2 == 0:  # Cross Shape
                            if state.players[n_player].quota[ShapeConstant.CROSS] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CROSS, GameConstant.PLAYER_COLOR[n_player])

                                state.board.set_piece(
                                    findBlankRow(i), i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] < best["val"]:
                                    best = alt

                                # Erase Move
                                # xxxxxxxxxx WIP

                        else:  # Circle Shape
                            if state.players[n_player].quota[ShapeConstant.CIRCLE] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CIRCLE, GameConstant.PLAYER_COLOR[n_player])

                                state.board.set_piece(
                                    findBlankRow(i), i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] < best["val"]:
                                    best = alt

                                # Erase Move
                                # xxxxxxxxxx WIP

            return best

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice(
            [ShapeConstant.CROSS, ShapeConstant.CIRCLE]))  # minimax algorithm

        return best_movement
