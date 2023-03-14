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
                    
            if i < BOARD_SIZE-4:
                for j in np.arange(BOARD_SIZE-3):
                    # Diagonal
                    value = np.diag(self.board, k=i)
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X':
                            return 1
                        elif value[j] == 'O':
                            return 2
                    
                    value = np.diag(self.board, k=i*-1)    
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X':
                            return 1
                        elif value[j] == 'O':
                            return 2
                    
                    # Reverse Diagonal
                    value = np.diag(np.fliplr(self.board), k=i)
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X':
                            return 1
                        elif value[j] == 'O':
                            return 2
                        
                    value = np.diag(np.fliplr(self.board), k=i*-1)
                    if np.unique(value[j:j+4]).size == 1:
                        if value[j] == 'X':
                            return 1
                        elif value[j] == 'O':
                            return 2
                    
        # Draw    
        if np.unique(self.board.ravel()).size == 2 and ' ' not in self.board.ravel():
            return 3
            
        return 0