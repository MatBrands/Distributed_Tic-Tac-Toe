from uuid import uuid4
from os import system
import platform
import Pyro5.client as Pyro5

BOARD_SIZE = 7

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

def is_a_win(winner: bool) -> bool:
    match winner:
        case 1:
            input(f'Player 1 wins')
        case 2:
            input(f'Player 2 wins')
        case 3:
            input(f'Draw')
        case _:
            return True
    return False

def clear() -> None:
    so = platform.system()
    if so == 'Windows':
        system('cls')
    else:
        system('clear')

if __name__ == '__main__':
    status = True
    client_id = str(uuid4())
    
    try:
        # ip = input('Server IP: ')
        # port = int(input('Server Port: '))
        ip, port = 'localhost', 46327
        game = Pyro5.Proxy(f"PYRO:Tic-Tac-Toe@{ip}:{port}")
        game._pyroHandshake = client_id
        game._pyroBind()
    except:
        print('Invalid server')
        exit()

    if client_id in game.get_player()[0]:
        print('You are player 1')
        play = 'X'
    else:
        print('You are player 2')
        play = 'O'

    input()
    
    while status:
        clear()
        
        status = is_a_win(game.check_win())
        
        if not game.can_play(play):
            print("Waiting for opponent's move...")
            clear()
        elif not status:
            break
        else:
            if play in 'X':
                print(f'Player 1, place the {play}')
            else:
                print(f'Player 2, place the {play}')
            
            board = game.get_board()
            print_board(board)
            
            while True:
                try:
                    x = int(input('X: '))
                    y = int(input('Y: '))
                except KeyboardInterrupt:
                    status = False
                    break
                except:
                    input('Invalid move')
                else:
                    if game.make_move(x, y, play): break
                    input('Invalid move')
    
    game._pyroRelease()