from uuid import uuid4
import Pyro5.client as Pyro5

BOARD_SIZE = 3

def print_board(board: list) -> None:
    print(f'   ', end=' ')
    for i in range(BOARD_SIZE):
        print (f'{i}   ', end='')
    print()
    for i in range(BOARD_SIZE):
        print(f'{i}  ', end='')
        for j in range(BOARD_SIZE):
            print(f'[{board[i][j]}]', end=' ')
        print()

if __name__ == '__main__':
    client_id = uuid4()
    
    game = Pyro5.Proxy("PYRO:hash_game@localhost:46327")
    game._pyroHandshake = client_id
    game._pyroBind()

    while True:
        for i in range (1, 3):
            print(f'Player {i}')
            
            board = game.get_board()
            print_board(board)
            
            while True:
                try:
                    x = int(input('X: '))
                    y = int(input('Y: '))
                except KeyboardInterrupt:
                    exit()
                except:
                    print('Invalid move')
                else:
                    if i == 1:
                        if game.player_1(x, y): break
                    else:
                        if game.player_2(x, y): break
                        
                    print('Invalid move')
            
            winner = game.check_win()
                    
            if winner == i:
                print(f'Player {i} wins')
                exit()
            elif winner == 3:
                print('Draw')
                exit()