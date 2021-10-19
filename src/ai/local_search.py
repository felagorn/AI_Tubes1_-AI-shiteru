from time import time
from src.model import State, Board, Player, Piece
from src.constant import ShapeConstant
from src.model import State
from typing import Tuple, List
import random
import copy
import datetime
import math

# Perubahan setelah dipindah dari bot.py
# 1. Nama kelas berubah dari Bot --> LSBot
# 2. ctor tidak lagi menerima is_minimax
# 3. Tidak lagi memakai best_movement
# 4. Nama method diubah dari __local_search -> local_search

class HeuristicGroup20:

    def __init__(self, board: Board, player: Player, enemy: Player):
        self.board = board
        self.player = player
        self.enemy = enemy

    ''' Meng-output nilai fungsi objektif '''
    def calculate_heuristic(self) -> float:
        h1 = self.__yellow_tile_heuristic()
        h2 = self.__streak_heuristic()
        h3 = self.__shape_heuristic()
        return h1 + h2 + h3

    ''' Heuristik 1: Yellow Tile '''
    def __yellow_tile_heuristic(self):
        # Heuristik kecil yang mendefinisikan tile yang lebih dominan
        h1 = 0
        c1 = 1
        for r in range(self.board.row):
            for c in range(self.board.col):
                current_piece = self.board.__getitem__(pos=(r,c))
                if  ((c == 3) or (r == 2) or (r == 3)) and (current_piece.shape != ShapeConstant.BLANK):
                    # Shape more dominant
                    if (current_piece.shape == self.player.shape):
                        h1 += 1.01
                    else:
                        h1 -= 1.01
                    # Color less dominant
                    if (current_piece.color == self.player.color):
                        h1 += 1
                    else:
                        h1 -= 1
        return c1 * h1

    ''' Heuristik 3: Shape '''
    
    def __shape_heuristic(self):
        # Heuristik keciiiiil yang membuat bot tidak menyimpan bidak shape lawan 
        h3 = 0
        c3 = 0.5
        for shape in self.player.quota:
            if shape == self.player.shape:
                h3 += self.player.quota[shape]
            else:
                h3 -= self.player.quota[shape]
        return c3 * h3
    
    ''' Heuristik 2: Streak '''

    def __streak_heuristic(self):
        return self.__vertical_streak() + self.__horizontal_streak() + self.__diagonalLTR_streak() + self.__diagonalRTL_streak()

    def __counter(self, boardCopy):
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
                if j >= len(boardCopy[i]):
                    break

                # Player Shape Counter
                elif boardCopy[i][j].shape == self.player.shape and self.player.quota[self.player.shape] > 0  :
                    StartPointer = j
                    Counter = 0
                    
                    while boardCopy[i][j].shape == self.player.shape:
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
                elif boardCopy[i][j].shape == self.enemy.shape and self.enemy.quota[self.enemy.shape] > 0  :
                    StartPointer = j
                    Counter = 0
                    while boardCopy[i][j].shape == self.enemy.shape   :
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
                if j >= len(boardCopy[i]):
                        break   
               
                # Player Color Counter  
                elif boardCopy[i][j].color==self.player.color:
                    StartPointer = j
                    Counter = 0
                    while boardCopy[i][j].color==self.player.color  :
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
                elif boardCopy[i][j].color==self.enemy.color:
                    StartPointer = j
                    Counter = 0
                    while boardCopy[i][j].color==self.enemy.color  :
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

    def __horizontal_streak(self):
        boardCopy = copy.deepcopy(self.board.board)
        return self.__counter(boardCopy)

    def __vertical_streak(self):
        boardCopy = [[0 for i in range(self.board.row)] for j in range(self.board.col)]
        for i in range(self.board.col):
            for j in range(self.board.row):
                boardCopy[i][j] = copy.deepcopy(self.board.board[j][i])
        return self.__counter(boardCopy)

   # def count_streak(board: Board):
    def __diagonalRTL_streak(self):
        # Diagonalisasi Board
        boardCopy =  [[] for i in range(self.board.col + self.board.row - 1)]
        for i in range(self.board.row):
            for j in range(self.board.col):
                boardCopy[i+j].append(copy.deepcopy(self.board.board[i][j]))
        return self.__counter(boardCopy)
      
    def __diagonalLTR_streak(self):
        # Diagonalisasi Board
        boardCopy =  [[] for i in range(self.board.col + self.board.row - 1)]
        for i in range(self.board.col):
            for j in range(self.board.row):
                boardCopy[i+j].append(copy.deepcopy(self.board.board[j][i]))
        return self.__counter(boardCopy)

class LSBotGroup20:

    ''' Constructor '''
    def __init__(self, state: State, n_player: int, thinking_time: float):
        self.state = state
        self.n_player = n_player
        self.thinking_time = thinking_time

    ''' Implementasikan algoritma local search di sini '''
    def local_search(self):

        # Menggunakan algoritma simulated annealing untuk menghasilkan tuple (int,str)
        # yang adalah representasi dari move yang dilakukan bot

        # Ambil waktu saat fungsi ini mulai dipanggil
        start = datetime.datetime.now()

        # Buat temperatur
        T = self.__get_temperature()

        # Hitung nilai heuristik board saat ini
        current_heuristic = HeuristicGroup20(board=self.state.board, player=self.state.players[self.n_player], enemy=self.state.players[(self.n_player+1)%2]).calculate_heuristic()

        # Generate neighbors
        neighbors = self.__generate_neighbors()

        # Selama thinking time < 3.9 detik...
        while ((datetime.datetime.now() - start) < datetime.timedelta(seconds = self.thinking_time-0.1)):

            # neighbor tu dictionary dengan key: movement(col: int, shape: str) sama heuristic: float
            neighbor = random.choice(neighbors)
            
            # Jika nilai heuristik neighbor lebih bagus dari current, pergi ke neighbor.
            # Kalau tidak, bandingkan nilai heuristic / T dengan bilangan random r di mana 0 ≤ r ≤ 1.
            # Jika heuristic / T > r, pergi ke neighbor.
            if (neighbor["heuristic"] > current_heuristic) or (math.exp((neighbor["heuristic"] - current_heuristic) / T) > random.random()):
                return neighbor["movement"]
        
        # time limit exceeded
        return random.choice(neighbors)["movement"]

    ''' ***** METHOD PEMBANTU __local_search ***** '''

    ''' Melakukan ekspansi pada state yang ada pada objek '''
    def __generate_neighbors(self):

        # Mengeluarkan array of map dengan 2 key yaitu movement dan heuristic. Movement
        # menyatakan langkah yang diambil dan berupa tuple (integer, string) dimana
        # integer melambangkan kolom peletakkan bidak dan string melambangkan shape
        # bidak yang diletakkan. Heuristic adalah nilai yang di generate dengan
        # menggunakan fungsi __calculate_heuristic dari masing-masing state
        # Neighbor yang di-generate diambil dari atribut state pada objek

        neighbors = []
        for col in range (self.state.board.col):
            # Cari row paling atas yang masih kosong
            row = self.state.board.row - 1
            while row >= 0 and (self.state.board.__getitem__(((self.state.board.row - 1) - row, col)).shape == ShapeConstant.BLANK):
                row -= 1
            row += 1
            
            # Pada row yang belum penuh, generate neighbor masing-masing dengan shape
            if row < self.state.board.row:
                for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                    # Jika shape di tangan player masih ada
                    if self.state.players[self.n_player].quota[shape] > 0:
                        current_neighbor = {}
                        current_neighbor["movement"] = (col, shape)
                        current_board = copy.deepcopy(self.state.board)

                        current_player = copy.deepcopy(self.state.players[self.n_player])
                        enemy_player = copy.deepcopy(self.state.players[(self.n_player+1)%2])
                        current_player.quota[shape] -= 1
                        # Taruh piece di board hasil deepcopy
                        current_board.set_piece((self.state.board.row - 1) - row, col, Piece(shape, self.state.players[self.n_player].color))
                        current_neighbor["heuristic"] = HeuristicGroup20(board = current_board, player = current_player, enemy=enemy_player).calculate_heuristic()

                        neighbors.append(current_neighbor)
        return neighbors

    ''' Mengeluarkan nilai temperatur berdasarkan nilai dari atribut objek state.round '''
    def __get_temperature(self, cooling_rate: float = 0.75, initial_temperature: float = 100):

        # Mengeluarkan nilai temperatur berdasar nilai dari atribut objek state.round
        # Semakin besar nilai round, maka hasil output akan semakin kecil

        return initial_temperature * (cooling_rate ** self.state.round)

class LocalSearchGroup20:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
 
        local_search_bot = LSBotGroup20(state = state, n_player = n_player, thinking_time = self.thinking_time)
        best_movement = local_search_bot.local_search() #local search algorithm

        return best_movement