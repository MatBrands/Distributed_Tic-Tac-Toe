from uuid import uuid4
from os import system
from time import sleep
import platform
import Pyro5.client as Pyro5

BOARD_SIZE = 7

def print_board(board: list) -> None:
    print(f'   ', end=' ')
    for i in range(BOARD_SIZE): print (f'{i}   ', end='')
    
    print()
    for i in range(BOARD_SIZE):
        print(f'{i}  ', end='')
        for j in range(BOARD_SIZE): print(f'[{board[i][j]}]', end=' ')
        print()

def is_a_win(winner: bool) -> bool:
    match winner:
        case 1|2: input(f'Player {winner} wins')
        case 3: input(f'Draw')
        case _: return True
    return False

def clear() -> None:
    so = platform.system()
    if so == 'Windows': system('cls')
    else: system('clear')

def tela_inicial(lobby, client_id: uuid4) -> None:
    print(f'Bem vindo ao jogo da velha online, seu id é: {client_id}')
    while True:
        print('1 - Observar salas\n2 - Criar sala\n3 - Entrar em uma sala\nOutra opção - Sair')
        
        option = input('Opção: ')
        match option:
            case '1':
                salas = lobby.get_waiting_room()
                if len(salas):
                    print('Salas disponíveis:')
                    for item in salas:
                        print(item)
                else:
                    print('Não há salas disponíveis')
                input('Pressione enter para continuar.\n')
            case '2':
                print('Criando sala...')
                lobby.add_to_waiting_room(client_id)
                print('Sala criada com sucesso!')
                input('Pressione enter para continuar.\n')
                break
            case '3':
                salas = lobby.get_waiting_room()
                if len(salas):
                    print('Salas disponíveis:')
                    for i, item in enumerate(salas):
                        print(f'{i} - {item}')
                    target = input('Qual sala deseja entrar?\n')
                    if target.isdigit() and 0 <= int(target) < len(salas):
                        target = int(target)
                        
                        clear()
                        print('Entrando na sala ', end='')
                        for i in range(3):
                            print(".", end="", flush=True)
                            sleep(1)
                        
                        lobby.match_players(client_id, salas[target])
                        break
                    else:
                        print('Opção inválida')
                        input('Pressione enter para continuar.\n')
                else:
                    print('Não há salas disponíveis')
                    input('Pressione enter para continuar.\n')
            case _: 
                lobby._pyroRelease()
                exit()
        clear()
    clear()
    return None

if __name__ == '__main__':
    clear()
    client_id = str(uuid4())
    
    try:
        # host = input('Server host: ')
        # port = int(input('Server Port: '))
        host, port = 'localhost', 46327
        lobby = Pyro5.Proxy(f"PYRO:Tic-Tac-Toe@{host}:{port}")
        lobby._pyroHandshake = client_id
        lobby._pyroBind()
    except:
        print('Erro ao conectar ao servidor')
        exit()

    tela_inicial(lobby, client_id)
    
    while True:
        uri = lobby.get_game(client_id)
        if uri: break
        else: 
            clear()
            print(f'Seu id é: {client_id}')
            print('Aguardando oponente', end=' ')
            for i in range(3):
                print(".", end="", flush=True)
                sleep(1)

    try:
        game = Pyro5.Proxy(uri)
        game._pyroBind()
    except:
        print('Erro ao conectar ao game')
        lobby._pyroRelease()
        exit()
        
    clear()
    if client_id in game.get_player()[0]:
        print('You are player 1'); play = 'X'
    else:
        print('You are player 2'); play = 'O'

    input('Pressione enter para continuar.\n')
    
    try:
        status = True
        while status:
            clear()
            
            status = is_a_win(game.check_win())
            
            if not game.can_play(play) and status:
                clear()
                print('Aguardando jogada do oponente', end=' ')
                for i in range(3):
                    print(".", end="", flush=True)
                    sleep(.5)
            elif not status:
                for item in game.get_player():
                    if item == -1:
                        input('Oponente saiu do jogo')
                break
            else:
                if play in 'X': i = 1
                else: i = 2
                
                print(f'Player {i}, posicione {play}')
                board = game.get_board()
                print_board(board)
                
                while True and status:
                    try:
                        x = int(input('X: '))
                        y = int(input('Y: '))
                    except KeyboardInterrupt:
                        status = False
                        game.quit_game(client_id)
                        game._pyroRelease()
                        lobby._pyroRelease()
                        break
                    except:
                        input('Movimento inválido')
                    else:
                        if game.make_move(x, y, play): break
                        input('Movimento inválido')
    except KeyboardInterrupt:
        game.quit_game(client_id)
        
    game._pyroRelease()
    lobby._pyroRelease()