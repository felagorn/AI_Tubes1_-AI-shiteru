from time import time
from src.model import State, Board, Player, Piece
from src.constant import ShapeConstant
from src.model import State
# from src.ai.bot import Bot
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

class LSBot:

    ''' Constructor '''
    def __init__(self, state: State, n_player: int, thinking_time: float): #, is_minimax: bool
        self.state = state
        self.n_player = n_player
        self.thinking_time = thinking_time
        # self.is_minimax = is_minimax
    
    ''' Meng-output nilai fungsi objektif '''
    def __calculate_heuristic(self, board: Board, player: Player, movement: Tuple[int, str] = (-1,'-'), ignore_movement: bool = False) -> float:
        
        h1 = self.__yellow_tile_heuristic(board)
        h3 = self.__shape_heuristic(player)
        print("h1 = "+ str(h1))
        print("h3 = " + str(h3))
        return h1 + h3

    ''' Heuristik 1: Yellow Tile '''
    def __yellow_tile_heuristic(self, board: Board):
        h1 = 0
        c1 = 1
        player_shape = self.state.players[self.n_player].shape
        player_color = self.state.players[self.n_player].color
        for r in range(board.row):
            for c in range(board.col):
                current_piece = board.__getitem__(pos=(r,c))
                if  ((c == 3) or (r == 2) or (r == 3)) and (current_piece.shape != ShapeConstant.BLANK):
                    if (current_piece.shape == player_shape):
                        h1 += 1
                    else:
                        h1 -= 1
                    if (current_piece.color == player_color):
                        h1 += 1
                    else:
                        h1 -= 1
        return c1 * h1

    ''' Heuristik 3: Shape '''
    def __shape_heuristic(self, player: Player):
        h3 = 0
        c3 = 0.5
        for shape in player.quota:
            if shape == player.shape:
                h3 += player.quota[shape]
            else:
                h3 -= player.quota[shape]
        return c3 * h3

    # ''' Fungsi yang dipanggil pada local_search.py dan minimax.py '''
    # def best_movement(self):
        # if self.is_minimax:
            # return self.__minimax()
        # else:
            # return self.__local_search()
    
    # ''' Implementasikan algoritma minimax di sini '''
    # def __minimax(self):
        # pass

    ''' Implementasikan algoritma local search di sini '''
    def local_search(self):

        # Menggunakan algoritma simulated annealing untuk menghasilkan tuple (int,str)
        # yang adalah representasi dari move yang dilakukan bot

        # Ambil waktu saat fungsi ini mulai dipanggil
        start = datetime.datetime.now()

        # Buat temperatur
        T = self.__get_temperature()

        # Hitung nilai heuristik board saat ini
        print("---------------------CURRENT HEURISTIC-------------------")
        current_heuristic = self.__calculate_heuristic(board = self.state.board, player = self.state.players[self.n_player], ignore_movement = True)

        print ("-------------GENERATE NEIGHBOR----------------")

        # Generate neighbors
        neighbors = self.__generate_neighbors()

        print ("-----------------------------")

        # Selama thinking time < 3.9 detik...
        while ((datetime.datetime.now() - start) < datetime.timedelta(seconds = self.thinking_time-0.1)):

            # neighbor tu dictionary dengan key: movement(col: int, shape: str) sama heuristic: float
            neighbor = random.choice(neighbors) 
            
            # Jika nilai heuristik neighbor lebih bagus dari current, pergi ke neighbor.
            # Kalau tidak, bandingkan nilai heuristic / T dengan bilangan random r di mana 0 ≤ r ≤ 1.
            # Jika heuristic / T > r, pergi ke neighbor.
            if (neighbor["heuristic"] > current_heuristic) or (math.exp((neighbor["heuristic"] - current_heuristic) / T) > random.random()):
                print("Selected neighbor: ",neighbor['heuristic'])
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
                        current_player.quota[shape] -= 1
                        # Taruh piece di board hasil deepcopy
                        current_board.set_piece(row, col, Piece(shape, self.state.players[self.n_player].color))
                        current_neighbor["heuristic"] = self.__calculate_heuristic(board=current_board, player=current_player, movement=(col, shape))
                        neighbors.append(current_neighbor)
        return neighbors

    ''' Mengeluarkan nilai temperatur berdasarkan nilai dari atribut objek state.round '''
    def __get_temperature(self, cooling_rate: float = 0.75, initial_temperature: float = 100):

        # Mengeluarkan nilai temperatur berdasar nilai dari atribut objek state.round
        # Semakin besar nilai round, maka hasil output akan semakin kecil

        return initial_temperature * (cooling_rate ** self.state.round)

class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
 
        local_search_bot = LSBot(state = state, n_player = n_player, thinking_time = self.thinking_time)
        best_movement = local_search_bot.local_search() #local search algorithm

        return best_movement