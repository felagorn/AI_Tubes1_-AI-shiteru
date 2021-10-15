import random
from time import time
from model.board import Board
from model.config import Config
from model.piece import Piece

from src.constant import ShapeConstant, ColorConstant, GameConstant
from src.model import State
from src.utility import is_out, is_win, is_full, place
from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def is_valid_position(self, board: Board, col: int):
        return board[0][col].shape ==  ShapeConstant.BLANK

    def get_valid_positions(self, state: State):
        valid_positions = []
        for col in range(state.board.col):
            if is_valid_position(state.board, col):
                valid_positions.append(col)
        return valid_positions

    def findBlankRow(self, state: State, col: int):
        for row in range(state.board.row - 1, -1, -1):
            if state.board[row, col].shape == ShapeConstant.BLANK:
                return row

        return -1

    def vertical_streak(state: State):
    # Asumsi: Pada board state belum ada yang menang

        total_value = 0
        for col in (state.board.col-1):
            column_streak_counter = 0

            if state.board.board[0][col].shape != ShapeConstant.BLANK:
                col += 1
            else:
                
                for player in (state.players):

                    player_streak_counter = 0
                    for prior in GameConstant.WIN_PRIOR:

                        shape_streak_counter = 0
                        color_streak_counter = 0

                        row = 0
                        switch = False
                        while (row < state.board.row and not switch):
                            pointer = row

                            while state.board.board[pointer][col].shape == ShapeConstant.BLANK: # advancing BLANK
                                    row += 1
                                    pointer += 1
                                    if row == state.board.row -1:
                                        break
                            
                            if prior == GameConstant.WIN_PRIOR[0]: # streak berdasarkan SHAPE
                                streak_shape = state.board[pointer+1][col].shape
                                while (state.board.board[row][col].shape == streak_shape):
                                    shape_streak_counter += 1
                                    row += 1
                                    if row == state.board.row -1:
                                            break

                            else: # streak berdasarkan COLOR
                                streak_color = state.board[pointer+1][col].color
                                while (state.board.board[row][col].color == streak_color):
                                    color_streak_counter += 1
                                    row += 1
                                    if row == state.board.row -1:
                                            break

                            row += 1
                        
                    if shape_streak_counter >= color_streak_counter:
                        player_streak_counter = shape_streak_counter
                    else:
                        player_streak_counter = color_streak_counter
                if player == state.players[0]:
                    column_streak_counter -= player_streak_counter * 100
                else:
                    column_streak_counter += player_streak_counter * 100
                
                total_value += column_streak_counter




    def horizontal_streak(board: Board):


    def count_streak(board: Board):

    
        

    def eval(self, state: State):
        return 1  # return format dictionary{move: ("col", "shape"), val: int}

    def minimax(self, state: State, n_player: int, thinking_time: float, depth: int, isMax: bool):
        score = eval(state)

        # Basis
        if depth == 0:  # If leaf node
            # return format dictionary{"move": ("col", "shape"), "val": int}
            return score

        if is_full(state.board):  # If terminal
            # return format dictionary{"move": ("col", "shape"), "val": int}
            return {"move": ("col", "shape"), "val": 0}

        # Recursion
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
                                emptyRow = findBlankRow(i)
                                state.board.set_piece(
                                    emptyRow, i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] > best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CROSS)

                                # Erase Move
                                state.players[n_player].quota[shape] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i, blankPiece)

                        else:  # Circle Shape
                            if state.players[n_player].quota[ShapeConstant.CIRCLE] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CIRCLE, GameConstant.PLAYER_COLOR[n_player])

                                emptyRow = findBlankRow(i)
                                state.board.set_piece(
                                    emptyRow, i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] > best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CIRCLE)

                                # Erase Move
                                state.players[n_player].quota[shape] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i, blankPiece)
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

                                emptyRow = findBlankRow(i)
                                state.board.set_piece(
                                    emptyRow, i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] < best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CROSS)

                                # Erase Move
                                state.players[n_player].quota[shape] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i, blankPiece)

                        else:  # Circle Shape
                            if state.players[n_player].quota[ShapeConstant.CIRCLE] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CIRCLE, GameConstant.PLAYER_COLOR[n_player])

                                emptyRow = findBlankRow(i)
                                state.board.set_piece(
                                    emptyRow, i, piece)

                                state.players[n_player].quota[shape] -= 1

                                # Recursive call
                                alt = minimax(state, (n_player+1) % 2,
                                              thinking_time, depth - 1,
                                              not isMax)
                                if alt["val"] < best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CIRCLE)

                                # Erase Move
                                state.players[n_player].quota[shape] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i, blankPiece)

            return best

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice(
            [ShapeConstant.CROSS, ShapeConstant.CIRCLE]))  # minimax algorithm

        return best_movement
