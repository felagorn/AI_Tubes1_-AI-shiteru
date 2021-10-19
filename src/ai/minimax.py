import random
from time import time
from src.model.board import Board
from src.model.config import Config
from src.model.piece import Piece

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
            if state.board.board[row][col].shape == ShapeConstant.BLANK:
                return row

        return -1

    def horizontal_streak(self, state: State, n_player:int):
        boardCopy = state.board.board

        return self.counter(state, n_player, boardCopy)

    def vertical_sreak(self, state: State, n_player: int):
        boardCopy = [[0 for i in range(state.board.row)] for j in range(state.board.col)]

        for i in range(state.board.col):
            for j in range(state.board.row):
                boardCopy[i][j] = state.board.board[j][i]

        return self.counter(state, n_player, boardCopy)

   # def count_streak(board: Board):
    def diagonalRTL_Streak(self,state:State,n_player:int):
        # Diagonalisasi Board
        boardCopy =  [[] for i in range(state.board.col + state.board.row - 1)]
        for i in range(state.board.row):
            for j in range( state.board.col):
                boardCopy[i+j].append(state.board.board[i][j])

        return self.counter(state, n_player,boardCopy)
        
   
      
    def diagonalLTR_Streak(self,state:State,n_player:int):
        # Diagonalisasi Board
        boardCopy =  [[] for i in range(state.board.col + state.board.row - 1)]
        for i in range(state.board.col):
            for j in range( state.board.row):
                boardCopy[i+j].append(state.board.board[j][i])

        return self.counter(state, n_player,boardCopy)
        

    def counter(self,state:State, n_player:int,boardCopy):
        # Inisialisasi Counter
        Player3StreakCounterSingleSide = 0
        Player3StreakCounterDoubleSide = 0
        Player2StreakCounterSingleSide = 0
        Player2StreakCounterDoubleSide = 0

        Enemy3StreakCounterSingleSide = 0
        Enemy3StreakCounterDoubleSide = 0
        Enemy2StreakCounterSingleSide = 0
        Enemy2StreakCounterDoubleSide = 0

        # Counting Shape
        for i in range(len(boardCopy)):
            j=0
            while j < len(boardCopy[i]):
                # While Blank
                if boardCopy[i][j].shape == ShapeConstant.BLANK:
                    while boardCopy[i][j].shape == ShapeConstant.BLANK:
                        j +=1
                        if j >= len(boardCopy[i]):
                            break

                # if J over Board
                elif j >= len(boardCopy[i]):
                        break  

                # Player Shape Counter
                elif boardCopy[i][j].shape == state.players[n_player].shape and state.players[n_player].quota[state.players[n_player].shape] > 0  :
                    StartPointer = j
                    Counter = 0
                    
                    while boardCopy[i][j].shape == state.players[n_player].shape   :
                        j += 1 
                        Counter += 1
                        if j >= len(boardCopy[i]):
                            break   
                    
                    if Counter == 2 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Player2StreakCounterDoubleSide += 1
                            else :
                                Player2StreakCounterSingleSide += 1

                    elif Counter == 3 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Player3StreakCounterDoubleSide += 1
                            else :
                                Player3StreakCounterSingleSide += 1
                                        
                # Enemy Shape
                elif boardCopy[i][j].shape == state.players[(n_player+1)%2].shape and state.players[(n_player+1)%2].quota[state.players[(n_player+1)%2].shape] > 0  :
                    StartPointer = j
                    Counter = 0
                    while boardCopy[i][j].shape == state.players[(n_player+1)%2].shape   :
                        j += 1 
                        Counter += 1
                        if j >= len(boardCopy[i]):
                            break   

                    if Counter == 2 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Enemy2StreakCounterDoubleSide += 1
                            else :
                                Enemy2StreakCounterSingleSide += 1

                    elif Counter == 3 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Enemy3StreakCounterDoubleSide += 1
                            else :
                                Enemy3StreakCounterSingleSide += 1

                else:
                    j += 1
               
        # Counting Colors
        for i in range(len(boardCopy)):
            j=0
            while j < len(boardCopy[i]):
                # While Blank
                if boardCopy[i][j].shape == ShapeConstant.BLANK:
                    while boardCopy[i][j].shape == ShapeConstant.BLANK:
                        j +=1
                        if j >= len(boardCopy[i]):
                            break

                # if j overboard        
                elif j >= len(boardCopy[i]):
                        break   
               
                # Player Color Counter  
                elif boardCopy[i][j].color==state.players[n_player].color:
                    StartPointer = j
                    Counter = 0
                    while boardCopy[i][j].color==state.players[n_player].color  :
                        j += 1 
                        Counter += 1
                        if j >= len(boardCopy[i]):
                            break   

                    if Counter == 2 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Player2StreakCounterDoubleSide += 1
                            else :
                                Player2StreakCounterSingleSide += 1

                    elif Counter == 3 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Player3StreakCounterDoubleSide += 1
                            else :
                                Player3StreakCounterSingleSide += 1
                

                # Enemy Color   
                elif boardCopy[i][j].color==state.players[(n_player+1)%2].color:
                    StartPointer = j
                    Counter = 0
                    while boardCopy[i][j].color==state.players[(n_player+1)%2].color  :
                        j += 1 
                        Counter += 1
                        if j >= len(boardCopy[i]):
                            break   

                    if Counter == 2 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Enemy2StreakCounterDoubleSide += 1
                            else :
                                Enemy2StreakCounterSingleSide += 1

                    elif Counter == 3 :
                        isHeadBlank = False
                        if StartPointer - 1 >0:
                            if boardCopy[i][StartPointer-1].shape == ShapeConstant.BLANK:
                                isHeadBlank = True
                        isTailBlank = False
                        if j + 1 < len(boardCopy[i]) :
                            if boardCopy[i][j + 1].shape == ShapeConstant.BLANK:
                                isTailBlank = True
                        if isHeadBlank or isTailBlank :
                            if isHeadBlank and isTailBlank :
                                Enemy3StreakCounterDoubleSide += 1
                            else :
                                Enemy3StreakCounterSingleSide += 1
                else:
                    j += 1
        
        total_score = (Player3StreakCounterSingleSide * 3
        + Player3StreakCounterDoubleSide * 10000
        + Player2StreakCounterSingleSide 
        + Player2StreakCounterDoubleSide * 2) 
        - (Enemy3StreakCounterSingleSide * 3
        + Enemy3StreakCounterDoubleSide * 10000
        + Enemy2StreakCounterSingleSide
        + Enemy2StreakCounterDoubleSide * 2) 
        return total_score

    def eval(self, state: State, n_player:int):
        return self.vertical_sreak(state, n_player) + self.horizontal_streak(state, n_player) + self.diagonalLTR_Streak(state, n_player) + self.diagonalRTL_Streak(state, n_player)

    def minimax(self, state: State, init_player: int, n_player: int, thinking_time: float, init_time:float, depth: int, isMax: bool,alpha:int,beta:int, prior_move):
        score = self.eval(state,n_player)

        # Basis
        if time() >= init_time + thinking_time - 0.5:
            if is_full(state.board):  # If terminal
                # return format dictionary{"move": prior_move, "val": int}
                return {"move": prior_move, "val": 0}

            winner = is_win(state.board)
            if winner:  
                if winner[0] ==  state.players[init_player].shape and winner[1] ==  state.players[init_player].color:
                    return {"move": prior_move, "val": 999999}
                else :
                    return {"move": prior_move, "val": -999999}
            else :
                return {"move": prior_move, "val": score}
        else:
            if is_full(state.board):  # If terminal
                # return format dictionary{"move": prior_move, "val": int}
                return {"move": prior_move, "val": 0}

            winner = is_win(state.board)
            if depth == 0 or winner:  # If leaf node
                # return format dictionary{"move": prior_move, "val": int}
                if winner:  
                    if winner[0] ==  state.players[init_player].shape and winner[1] ==  state.players[init_player].color:
                        return {"move": prior_move, "val": 999999}
                    else :
                        return {"move": prior_move, "val": -999999}
                else :
                    return {"move": prior_move, "val": score}
        

            # Recursion
            if (isMax):  # Maximizer
                best = {"move": prior_move, "val": -999999}

                # traverse movement
                for i in range(state.board.col*2):
                    
                    emptyRow = self.findBlankRow(state,i % state.board.col)
                    if emptyRow != -1:
                        if i <state.board.col:  # Cross Shape
                            if state.players[n_player].quota[ShapeConstant.CROSS] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CROSS, GameConstant.PLAYER_COLOR[n_player])
                                
                                state.board.set_piece(
                                    emptyRow, i, piece)

                                state.players[n_player].quota[ShapeConstant.CROSS] -= 1
                                
                                # Recursive call
                                alt = self.minimax(state, init_player, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax, alpha,beta, (i, ShapeConstant.CROSS))
                                if alt["val"] > best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CROSS)

                                #print(best["val"], ": ", best["move"])
                                # Erase Move
                                state.players[n_player].quota[ShapeConstant.CROSS] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i % state.board.col, blankPiece)

                                

                                alpha = max(alpha, best["val"])
                                if alpha >= beta:
                                    break

                                
                               

                        else:  # Circle Shape
                            if state.players[n_player].quota[ShapeConstant.CIRCLE] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CIRCLE, GameConstant.PLAYER_COLOR[n_player])

                            
                                state.board.set_piece(
                                    emptyRow, i % state.board.col, piece)

                                state.players[n_player].quota[ShapeConstant.CIRCLE] -= 1
                                
                                # Recursive call
                                alt = self.minimax(state, init_player, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax,alpha,beta,(i % state.board.col, ShapeConstant.CIRCLE))
                                if alt["val"] > best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i % state.board.col, ShapeConstant.CIRCLE)

                                # Erase Move
                                #print(best["val"], ": ", best["move"])
                                state.players[n_player].quota[ShapeConstant.CIRCLE] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i % state.board.col, blankPiece)

                                

                                alpha = max(alpha, best["val"])
                                if alpha >= beta:
                                    break

                                
                
                return best 
            else:  # Minimizer
                best = {"move": prior_move, "val": 999999}
                # traverse movement
                for i in range(state.board.col * 2):
                    emptyRow = self.findBlankRow(state,i % state.board.col)
                    if emptyRow != -1:
                        if i <state.board.col:  # Cross Shape
                            if state.players[n_player].quota[ShapeConstant.CROSS] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CROSS, GameConstant.PLAYER_COLOR[n_player])

                                
                                state.board.set_piece(
                                    emptyRow, i, piece)

                                state.players[n_player].quota[ShapeConstant.CROSS] -= 1

                                

                                # Recursive call
                                alt = self.minimax(state, init_player, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax,alpha,beta, (i, ShapeConstant.CROSS))
                                if alt["val"] < best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CROSS)

                                # Erase Move
                                #print(best["val"], ": ", best["move"])
                                state.players[n_player].quota[ShapeConstant.CROSS] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i % state.board.col, blankPiece)

                                

                                beta = min(beta, best["val"])
                                if alpha >= beta:
                                    break
                                

                        else:  # Circle Shape
                            if state.players[n_player].quota[ShapeConstant.CIRCLE] != 0:
                                # Make the move
                                piece = Piece(
                                    ShapeConstant.CIRCLE, GameConstant.PLAYER_COLOR[n_player])

                                
                                state.board.set_piece(
                                    emptyRow, i % state.board.col, piece)

                                state.players[n_player].quota[ShapeConstant.CIRCLE] -= 1

                                

                                # Recursive call
                                alt = self.minimax(state, init_player, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax,alpha,beta,(i % state.board.col, ShapeConstant.CIRCLE))
                                if alt["val"] < best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i % state.board.col, ShapeConstant.CIRCLE)

                                # Erase Move
                                #print(best["val"], ": ", best["move"])
                                state.players[n_player].quota[ShapeConstant.CIRCLE] += 1

                                blankPiece = Piece(
                                    ShapeConstant.BLANK, ColorConstant.BLACK)
                                state.board.set_piece(
                                    emptyRow, i % state.board.col, blankPiece)

                                
                                
                                beta = min(beta, best["val"])
                                if alpha >= beta:
                                    break

                                
                
                
                return best

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        time_start = time()
        
        value = self.minimax(state, n_player, n_player, thinking_time, time_start, 3, True,-999999,999999, None)
        best_movement = value["move"]  # minimax algorithm
        print(value["val"])
        print(value["move"])
        return best_movement
