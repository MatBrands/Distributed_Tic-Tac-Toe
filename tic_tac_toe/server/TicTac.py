import numpy as np
import Pyro5.server as Pyro5

BOARD_SIZE = 7

@Pyro5.expose
class TicTac:
    def __init__(self) -> None:
        self.reset_board()
        
    def reset_board(self) -> None:
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), ' ')
            
    def get_board(self) -> np:
        return self.board.tolist()
            
    def play(self, x: int, y: int, char: str) -> bool:
        if x < 0 or x > BOARD_SIZE-1 or y < 0 or y > BOARD_SIZE-1:
            return False
        
        if self.board[x, y] == ' ':
            self.board[x, y] = char
            return True
        else:
            return False
        
    def check_win(self) -> int:
        for i in np.arange(BOARD_SIZE):
            for j in np.arange(BOARD_SIZE-3):
                # Rows
                if np.unique(self.board[i, j:j+4]).size == 1:
                    if self.board[i, j] == 'X':
                        return 1
                    elif self.board[i, j] == 'O':
                        return 2

                # Columns
                if np.unique(self.board[j:j+4, i]).size == 1:
                    if self.board[j, i] == 'X':
                        return 1
                    elif self.board[j, i] == 'O':
                        return 2
                    
            if i < BOARD_SIZE-3:
                if np.unique(self.board.diagonal(0)[i:i+4]).size == 1:
                    if self.board.diagonal(0)[i] == 'X':
                        return 1
                    elif self.board.diagonal(0)[i] == 'O':
                        return 2
                    
                # Reverse Diagonal            
                if np.unique(np.fliplr(self.board).diagonal(0)[i:i+4]).size == 1:
                    if np.fliplr(self.board).diagonal(0)[i] == 'X':
                        return 1
                    elif np.fliplr(self.board).diagonal(0)[i] == 'O':
                        return 2
                
        # Draw    
        if np.unique(self.board.ravel()).size == 2 and ' ' not in self.board.ravel():
            return 3
            
        return 0