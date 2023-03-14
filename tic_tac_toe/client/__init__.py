from uuid import uuid4
from os import system
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

if __name__ == '__main__':
    client_id = uuid4()
    
    try:
        ip = input('Server IP: ')
        port = int(input('Server Port: '))
        game = Pyro5.Proxy(f"PYRO:Tic-Tac-Toe@{ip}:{port}")
        game._pyroHandshake = client_id
        game._pyroBind()
    except:
        print('Invalid server')
        exit()

    if str(client_id) in game.get_player()[0]:
        print('You are player 1')
        play = 'X'
    else:
        print('You are player 2')
        play = 'O'

    input()

    while True:
        system('clear')
        
        winner = game.check_win()
            
        match winner:
            case 1:
                input(f'Player 1 wins')
                break
            case 2:
                input(f'Player 2 wins')
                break
            case 3:
                input(f'Draw')
                break
        
        while not game.can_play(play):
            winner = game.check_win()
            
            match winner:
                case 1:
                    input(f'Player 1 wins')
                    exit()
                case 2:
                    input(f'Player 2 wins')
                    exit()
                case 3:
                    input(f'Draw')
                    exit()
            print("Waiting for opponent's move...")
            
            system('clear')
            
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
                exit()
            except:
                input('Invalid move')
            else:
                if game.make_move(x, y, play): break
                    
                input('Invalid move')