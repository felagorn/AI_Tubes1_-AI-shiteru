from src.model import State, Board, Player, Piece
from src.constant import ShapeConstant
from typing import Tuple
import random
import copy
import datetime
import math

class Bot:

    ''' Constructor '''
    def __init__(self, state: State, n_player: int, thinking_time: float, is_minimax: bool):
        self.state = state
        self.n_player = n_player
        self.thinking_time = thinking_time
        self.is_minimax = is_minimax
    
    ''' Meng-output nilai fungsi objektif '''
    def __calculate_heuristic(self, board: Board, movement: Tuple[int, str] = (-1,'-'), ignore_movement: bool = False) -> float:
        return random.random()

    ''' Fungsi yang dipanggil pada local_search.py dan minimax.py '''
    def best_movement(self):
        if self.is_minimax:
            return self.__minimax()
        else:
            return self.__local_search()
    
    ''' Implementasikan algoritma minimax di sini '''
    def __minimax(self):
        pass

    ''' Implementasikan algoritma local search di sini '''
    def __local_search(self):

        # Menggunakan algoritma simulated annealing untuk menghasilkan tuple (int,str)
        # yang adalah representasi dari move yang dilakukan bot

        # Ambil waktu saat fungsi ini mulai dipanggil
        start = datetime.datetime.now()

        # Buat temperatur
        T = self.__get_temperature()

        # Hitung nilai heuristik board saat ini
        current_heuristic = self.__calculate_heuristic(board = self.state.board, ignore_movement = True)

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
                        # Taruh piece di board hasil deepcopy
                        current_board.set_piece(row, col, Piece(shape, self.state.players[self.n_player].color))
                        current_neighbor["heuristic"] = self.__calculate_heuristic(current_board, (col, shape))
                        neighbors.append(current_neighbor)
        return neighbors

    ''' Mengeluarkan nilai temperatur berdasarkan nilai dari atribut objek state.round '''
    def __get_temperature(self, cooling_rate: float = 0.95, initial_temperature: float = 100):

        # Mengeluarkan nilai temperatur berdasar nilai dari atribut objek state.round
        # Semakin besar nilai round, maka hasil output akan semakin kecil

        return initial_temperature * (cooling_rate ** self.state.round)
