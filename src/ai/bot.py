from src.model import State, Board, Player

class Bot:

    ''' Constructor '''
    def __init__(self, state: State, n_player: int, thinking_time: float, is_minimax: bool):
        self.state = state
        self.n_player = n_player
        self.thinking_time = thinking_time
        self.is_minimax = is_minimax
    
    ''' Meng-output nilai fungsi objektif '''
    def __calculate_heuristic(self, board: Board, player: Player) -> bool:
        pass

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
        pass

    ''' ***** METHOD PEMBANTU __local_search ***** '''

    ''' Melakukan ekspansi pada state yang ada pada objek '''
    def __generate_neighbors(self):
        pass

    ''' Mengeluarkan nilai temperatur berdasarkan nilai dari atribut objek state.round '''
    def __get_temperature(self):
        pass