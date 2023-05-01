import numpy as np
import Pyro5.server as Pyro5

BOARD_SIZE = 7

@Pyro5.expose
class TicTac:
    def __init__(self, player_1: str, player_2: str) -> None:
        self.player = []
        self.__set_player(player_1); self.__set_player(player_2)
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), ' ')
        self.current_player = 'X'
            
    def change_game(self) -> None:
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), ' ')
        self.player = [self.player[1], self.player[0]]
            
    def __set_player(self, player: str) -> None:
        if player not in self.player:
            self.player.append(player)
        
    def get_player(self) -> list:
        return self.player
            
    def get_board(self) -> np:
        return self.board.tolist()
            
    def can_play(self, player:str) -> bool:
        if self.current_player == player:
            return True
        else:
            return False
            
    def make_move(self, x: int, y: int, char: str) -> bool:
        if x < 0 or x > BOARD_SIZE-1 or y < 0 or y > BOARD_SIZE-1:
            return False
        
        if self.board[x, y] == ' ':
            if self.current_player == 'X': self.current_player = 'O'
            else: self.current_player = 'X'
                
            self.board[x, y] = char
            return True
        else:
            return False
        
    def check_win(self) -> int:
        for i in np.arange(BOARD_SIZE):
            for j in np.arange(BOARD_SIZE-3):
                # Rows
                if np.unique(self.board[i, j:j+4]).size == 1:
                    if self.board[i, j] == 'X': return 1
                    elif self.board[i, j] == 'O': return 2

                # Columns
                if np.unique(self.board[j:j+4, i]).size == 1:
                    if self.board[j, i] == 'X': return 1
                    elif self.board[j, i] == 'O': return 2
                    
            if i < BOARD_SIZE-4:
                for j in np.arange(BOARD_SIZE-3):
                    # Diagonal
                    value = np.diag(self.board, k=i)
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X': return 1
                        elif value[j] == 'O': return 2
                    
                    value = np.diag(self.board, k=i*-1)    
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X': return 1
                        elif value[j] == 'O': return 2
                    
                    # Reverse Diagonal
                    value = np.diag(np.fliplr(self.board), k=i)
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X': return 1
                        elif value[j] == 'O': return 2
                        
                    value = np.diag(np.fliplr(self.board), k=i*-1)
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X': return 1
                        elif value[j] == 'O': return 2
                    
        # Draw    
        if ' ' not in self.board.ravel(): return 3

        return 0