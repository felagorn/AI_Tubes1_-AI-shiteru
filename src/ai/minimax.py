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

    def vertical_streak(state: State):
    # Asumsi: Pada board state belum ada yang menang

        total_value = 0
        for col in (state.board.col):
        # Iterasi setiap kolom pada board
            
            column_streak_counter = 0

            if state.board.board[0][col].shape != ShapeConstant.BLANK:
            # Kolom sudah penuh sampai baris atas
                col += 1
            else:
            # Kolom belum penuh
                # for player in (state.players):
                # Iterasi untuk menghitung streak player pada kolom yang bersangkutan

                # player_streak_counter = 0
                # for prior in GameConstant.WIN_PRIOR:
                # Iterasi untuk menghitung streak berdasarkan SHAPE dan COLOR
                shape_streak_counter = 0
                color_streak_counter = 0

                row = 0
                while (row < state.board.row):
                    pointer = row # pointer untuk menghitung indeks terakhir BLANK pada board

                    while state.board.board[pointer][col].shape == ShapeConstant.BLANK and row < state.board.row: # advancing BLANK
                        # if : # pointer sampai ke baris paling bawah -> kolom kosong
                        #     break
                        row += 1
                        pointer += 1
                    
                    if row >= state.board.row: # row sampai ke baris paling bawah -> kolom kosong
                        break

                    #row += 1 # row tepat di bawah pointer BLANK terakhir
                    
                    #if state.board.board[row][col].shape == GameConstant.WIN_PRIOR[0]: # streak berdasarkan SHAPE
                    streak_shape = state.board.board[row][col].shape
                    streak_color = state.board.board[row][col].color

                    while (state.board.board[row][col].shape == streak_shape and row < state.board.row):
                        shape_streak_counter += 1
                        row += 1
                    
                    row = 0
                    while state.board.board[row][col].color == streak_color and row < state.board.row:
                        color_streak_counter += 1
                        row += 1

                    if row >= state.board.row:
                        break

                    # else: # streak berdasarkan COLOR
                    # while (state.board.board[row][col].color == streak_color):
                    #     color_streak_counter += 1

                    #     if row >= state.board.row:
                    #         break
                    #     row += 1

                    row += 1
                    
                if shape_streak_counter >= color_streak_counter:
                    if streak_shape == state.players[0].shape:
                        column_streak_counter += shape_streak_counter * 100
                    elif streak_shape == state.players[1].shape:
                        column_streak_counter -= shape_streak_counter * 100

                else:
                    if streak_color == state.players[0].color:
                        column_streak_counter += color_streak_counter * 100
                    elif streak_color == state.players[1].color:
                        column_streak_counter -= color_streak_counter * 100
                #if player == state.players[0]:
                #else:
                
            total_value += column_streak_counter

        return total_value


    def horizontal_streak(state: State):

        shape_streak = 0
        color_streak = 0

        #for player in state.players:

        #player_streak = 0

        for prior in GameConstant.WIN_PRIOR:

            if prior == GameConstant.WIN_PRIOR[0]: # streak berdasarkan SHAPE

                # shape_streak = 0

                for row in state.board.row:

                    row_streak = 0

                    col = 0
                    while col < state.board.col:
                        streak_count = 0
                        while state.board.board[row][col].shape == ShapeConstant.BLANK and col < state.board.col: # advancing BLANK
                            col += 1
                            
                        if col >= state.board.col: # baris kosong
                            break

                        streak_shape = state.board.board[row][col].shape
                        streak_start_point = row
                        while state.board.board[row][col].shape == streak_shape and col < state.board.col:
                            streak_count += 1

                            col += 1
                        streak_end_point = row

                        if streak_shape == state.players[0].shape:
                            utility_factor = 1
                        elif streak_shape == state.players[1].shape:
                            utility_factor = -1

                        if streak_count == 4:
                            row_streak += 1000000 * utility_factor
                        elif streak_count == 3:
                            if streak_start_point - 1 >= 0 and streak_end_point + 1 < state.board.col:
                            # kedua titik samping ujung streak berada di dalam board
                                if  row == findBlankRow(state, streak_start_point-1) and row == findBlankRow(state, streak_end_point+1):
                                # kedua titik samping ujung streak kosong
                                    row_streak += 20000 * utility_factor
                                elif row == findBlankRow(state, streak_start_point-1):
                                # hanya titik samping ujung kiri streak saja yang kosong
                                    row_streak += 10000 * utility_factor
                                elif row == findBlankRow(state, streak_end_point+1):
                                # hanya titik samping ujung kanan streak saja yang kosong
                                    row_streak += 10000 * utility_factor
                            if streak_start_point - 1 >= 0:
                            # hanya titik samping ujung kiri streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_start_point - 1):
                                    row_streak += 10000 * utility_factor
                            if streak_end_point + 1 < state.board.col:
                            # hanya titik samping ujung kanan streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_end_point + 1):
                                    row_streak += 10000 * utility_factor
                        elif streak_count == 2:
                            if streak_start_point - 1 >= 0 and streak_end_point + 1 < state.board.col:
                            # kedua titik samping ujung streak berada di dalam board
                                if  row == findBlankRow(state, streak_start_point-1) and row == findBlankRow(state, streak_end_point+1):
                                # kedua titik samping ujung streak kosong
                                    row_streak += 2000 * utility_factor
                                elif row == findBlankRow(state, streak_start_point-1):
                                # hanya titik samping ujung kiri streak saja yang kosong
                                    row_streak += 1000 * utility_factor
                                elif row == findBlankRow(state, streak_end_point+1):
                                # hanya titik samping ujung kanan streak saja yang kosong
                                    row_streak += 1000 * utility_factor
                            if streak_start_point - 1 >= 0:
                            # hanya titik samping ujung kiri streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_start_point - 1):
                                    row_streak += 1000 * utility_factor
                            if streak_end_point + 1 < state.board.col:
                            # hanya titik samping ujung kanan streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_end_point + 1):
                                    row_streak += 1000 * utility_factor
                        elif streak_count == 1:
                            if streak_start_point - 1 >= 0 and streak_end_point + 1 < state.board.col:
                            # kedua titik samping ujung streak berada di dalam board
                                if  row == findBlankRow(state, streak_start_point-1) and row == findBlankRow(state, streak_end_point+1):
                                # kedua titik samping ujung streak kosong
                                    row_streak += 200 * utility_factor
                                elif row == findBlankRow(state, streak_start_point-1):
                                # hanya titik samping ujung kiri streak saja yang kosong
                                    row_streak += 100 * utility_factor
                                elif row == findBlankRow(state, streak_end_point+1):
                                # hanya titik samping ujung kanan streak saja yang kosong
                                    row_streak += 100 * utility_factor
                            if streak_start_point - 1 >= 0:
                            # hanya titik samping ujung kiri streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_start_point - 1):
                                    row_streak += 100 * utility_factor
                            if streak_end_point + 1 < state.board.col:
                            # hanya titik samping ujung kanan streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_end_point + 1):
                                    row_streak += 100 * utility_factor

                        if col >= state.board.col: # udah sampai kolom akhir dari baris yang bersangkutan
                            break

                        #col += 1
                    
                    shape_streak += row_streak

            elif prior == GameConstant.WIN_PRIOR[1]: # streak berdasarkan COLOR

                # color_streak = 0

                for row in state.board.row:

                    row_streak = 0

                    col = 0
                    while col < state.board.col:
                        streak_count = 0
                        while state.board.board[row][col].shape == ShapeConstant.BLANK and col < state.board.col: # advancing BLANK
                            col += 1
                            
                        if col >= state.board.col: # baris kosong
                            break

                        streak_color = state.board.board[row][col].color
                        streak_start_point = row
                        while state.board.board[row][col].color == streak_color and col < state.board.col:
                            streak_count += 1

                            col += 1
                        streak_end_point = row

                        if streak_color == state.players[0].color:
                            utility_factor = 1
                        elif streak_color == state.players[1].color:
                            utility_factor = -1

                        if streak_count == 4:
                            row_streak += 1000000 * utility_factor
                        elif streak_count == 3:
                            if streak_start_point - 1 >= 0 and streak_end_point + 1 < state.board.col:
                            # kedua titik samping ujung streak berada di dalam board
                                if  row == findBlankRow(state, streak_start_point-1) and row == findBlankRow(state, streak_end_point+1):
                                # kedua titik samping ujung streak kosong
                                    row_streak += 20000 * utility_factor
                                elif row == findBlankRow(state, streak_start_point-1):
                                # hanya titik samping ujung kiri streak saja yang kosong
                                    row_streak += 10000 * utility_factor
                                elif row == findBlankRow(state, streak_end_point+1):
                                # hanya titik samping ujung kanan streak saja yang kosong
                                    row_streak += 10000 * utility_factor
                            if streak_start_point - 1 >= 0:
                            # hanya titik samping ujung kiri streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_start_point - 1):
                                    row_streak += 10000 * utility_factor
                            if streak_end_point + 1 < state.board.col:
                            # hanya titik samping ujung kanan streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_end_point + 1):
                                    row_streak += 10000 * utility_factor
                        elif streak_count == 2:
                            if streak_start_point - 1 >= 0 and streak_end_point + 1 < state.board.col:
                            # kedua titik samping ujung streak berada di dalam board
                                if  row == findBlankRow(state, streak_start_point-1) and row == findBlankRow(state, streak_end_point+1):
                                # kedua titik samping ujung streak kosong
                                    row_streak += 2000 * utility_factor
                                elif row == findBlankRow(state, streak_start_point-1):
                                # hanya titik samping ujung kiri streak saja yang kosong
                                    row_streak += 1000 * utility_factor
                                elif row == findBlankRow(state, streak_end_point+1):
                                # hanya titik samping ujung kanan streak saja yang kosong
                                    row_streak += 1000 * utility_factor
                            if streak_start_point - 1 >= 0:
                            # hanya titik samping ujung kiri streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_start_point - 1):
                                    row_streak += 1000 * utility_factor
                            if streak_end_point + 1 < state.board.col:
                            # hanya titik samping ujung kanan streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_end_point + 1):
                                    row_streak += 1000 * utility_factor
                        elif streak_count == 1:
                            if streak_start_point - 1 >= 0 and streak_end_point + 1 < state.board.col:
                            # kedua titik samping ujung streak berada di dalam board
                                if  row == findBlankRow(state, streak_start_point-1) and row == findBlankRow(state, streak_end_point+1):
                                # kedua titik samping ujung streak kosong
                                    row_streak += 200 * utility_factor
                                elif row == findBlankRow(state, streak_start_point-1):
                                # hanya titik samping ujung kiri streak saja yang kosong
                                    row_streak += 100 * utility_factor
                                elif row == findBlankRow(state, streak_end_point+1):
                                # hanya titik samping ujung kanan streak saja yang kosong
                                    row_streak += 100 * utility_factor
                            if streak_start_point - 1 >= 0:
                            # hanya titik samping ujung kiri streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_start_point - 1):
                                    row_streak += 100 * utility_factor
                            if streak_end_point + 1 < state.board.col:
                            # hanya titik samping ujung kanan streak saja yang berada di dalam board
                                if row == findBlankRow(state, streak_end_point + 1):
                                    row_streak += 100 * utility_factor

                        if col >= state.board.col: # udah sampai kolom akhir dari baris yang bersangkutan
                            break

                        #col += 1
                    
                    color_streak += row_streak

        if shape_streak >= color_streak:
            return shape_streak
        else:
            return color_streak

        # for row in state.board.row:
            
        #     row_streak_counter = 0

        #     # Harus simpen indeks kolom streak awal dan akhir

        #     # for player in state.players:
        #     col = 0
        #     while col < state.board.col:
                
        #         shape_streak_counter = 0
        #         color_streak_counter = 0

        #         while state.board.board[row][col].shape == ShapeConstant.BLANK and col < state.board.col: # Advancing BLANK
        #             col += 1

        #         if col == state.board.col: # Udah sampe kolom terakhir baris -> kolom dari baris BLANK semua
        #             break

        #         streak_shape = state.board.board[row][col].shape
        #         streak_color = state.board.board[row][col].color

        #         if streak_shape == state.players[0].shape

        #         prior_point = col - 1
        #         while state.board.board[row][col].shape == streak_shape and col < state.board.col:
        #             shape_streak_counter += 1
        #             col += 1
        #         next_point = col + 1

        #         prior_is_blank = state.board.board[row][prior_point].shape == ShapeConstant.BLANK
        #         next_is_blank = state.board.board[row][next_point] == ShapeConstant.BLANK
        #         if  prior_is_blank or next_is_blank:
        #             if streak_shape
        #             row_streak_counter += 

                
        #         if col >= state.board.col:
        #             break

        #         col += 1


            
        #     total_value = 
                




   # def count_streak(board: Board):
    def diagonalRTL_Streak(self,state:State,n_player:int):
        # Diagonalisasi Board
        boardCopy =  [[] for i in range(state.board.col + state.board.row - 1)]
        for i in range(state.board.row):
            for j in range( state.board.col):
                boardCopy[i+j].append(state.board.board[i][j])

        # Inisialisasi Counter
        Player3StreakCounterSingleSide = 0
        Player3StreakCounterDoubleSide = 0
        Player2StreakCounterSingleSide = 0
        Player2StreakCounterDoubleSide = 0

        Enemy3StreakCounterSingleSide = 0
        Enemy3StreakCounterDoubleSide = 0
        Enemy2StreakCounterSingleSide = 0
        Enemy2StreakCounterDoubleSide = 0

        #Counting
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
        + Player3StreakCounterDoubleSide * 999999
        + Player2StreakCounterSingleSide 
        + Player2StreakCounterDoubleSide * 2) 
        - (Enemy3StreakCounterSingleSide * 3
        + Enemy3StreakCounterDoubleSide * 999999
        + Enemy2StreakCounterSingleSide 
        + Enemy2StreakCounterDoubleSide * 2) 
        return total_score
        

     
   
        
    def diagonalLTR_Streak(self,state:State,n_player:int):
        # Diagonalisasi Board
        boardCopy =  [[] for i in range(state.board.col + state.board.row - 1)]
        for i in range(state.board.col):
            for j in range( state.board.row):
                boardCopy[i+j].append(state.board.board[j][i])

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
        + Player3StreakCounterDoubleSide * 999999
        + Player2StreakCounterSingleSide 
        + Player2StreakCounterDoubleSide * 2) 
        - (Enemy3StreakCounterSingleSide * 3
        + Enemy3StreakCounterDoubleSide * 999999
        + Enemy2StreakCounterSingleSide
        + Enemy2StreakCounterDoubleSide * 2) 
        return total_score
        

     


      

    def eval(self, state: State, n_player:int):
        return self.diagonalLTR_Streak(state, n_player) + self.diagonalRTL_Streak(state, n_player)

    def minimax(self, state: State, n_player: int, thinking_time: float, init_time:float, depth: int, isMax: bool,alpha:int,beta:int):
        score = self.eval(state,n_player)

        # Basis
        if time() >= init_time + thinking_time - 0.5:
            if is_full(state.board):  # If terminal
                # return format dictionary{"move": ("col", "shape"), "val": int}
                return {"move": ("col", "shape"), "val": 0}

            winner = is_win(state.board)
            if winner:  
                if winner[0] ==  state.players[n_player].shape and winner[1] ==  state.players[n_player].color:
                    return {"move": ("col", "shape"), "val": 999999}
                else :
                    return {"move": ("col", "shape"), "val": -999999}
            else :
                return {"move": ("col", "shape"), "val": score}
        else:
            if is_full(state.board):  # If terminal
                # return format dictionary{"move": ("col", "shape"), "val": int}
                return {"move": ("col", "shape"), "val": 0}

            winner = is_win(state.board)
            if depth == 0 or winner:  # If leaf node
                # return format dictionary{"move": ("col", "shape"), "val": int}
                if winner:  
                    if winner[0] ==  state.players[n_player].shape and winner[1] ==  state.players[n_player].color:
                        return {"move": ("col", "shape"), "val": 999999}
                    else :
                        return {"move": ("col", "shape"), "val": -999999}
                else :
                    return {"move": ("col", "shape"), "val": score}
        

            # Recursion
            if (isMax):  # Maximizer
                best = {"move": ("col", "shape"), "val": -999999}

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
                                alt = self.minimax(state, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax, alpha,beta)
                                if alt["val"] > best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CROSS)

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
                                alt = self.minimax(state, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax,alpha,beta)
                                if alt["val"] > best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i % state.board.col, ShapeConstant.CIRCLE)

                                # Erase Move
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
                best = {"move": ("col", "shape"), "val": 999999}
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
                                alt = self.minimax(state, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax,alpha,beta)
                                if alt["val"] < best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i, ShapeConstant.CROSS)

                                # Erase Move
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
                                alt = self.minimax(state, (n_player+1) % 2,
                                                thinking_time,init_time, depth - 1,
                                                not isMax,alpha,beta)
                                if alt["val"] < best["val"]:
                                    best["val"] = alt["val"]
                                    best["move"] = (i % state.board.col, ShapeConstant.CIRCLE)

                                # Erase Move
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
        
        value = self.minimax(state, n_player, thinking_time, time_start,5, True,-999999,999999)
        
        best_movement = value["move"]  # minimax algorithm
       
        return best_movement
