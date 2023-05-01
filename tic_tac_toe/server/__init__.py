import Pyro5.server as Pyro5
from src.Lobby import Lobby

class Server:
    def __init__(self, daemon: Pyro5.Daemon) -> None:
        self._client_id_by_connection = {}
        self.daemon = daemon
        self.lobby = Lobby(daemon)

    def client_connected(self, connection: Pyro5, client_id: str) -> None:
        if client_id not in 'hello':
            print(f"Cliente: {client_id} conectado")
        self._client_id_by_connection[connection] = client_id

    def client_disconnected(self, connection: Pyro5) -> None:
        client_id = self._client_id_by_connection[connection]
        if client_id in self.lobby.waiting_room:
            self.lobby.remove_from_waiting_room(client_id)
        for game in self.lobby.lobby:
            if client_id in game.player:
                self.lobby.remove_from_lobby(game)
        
        if client_id not in 'hello':
            print(f"Cliente: {client_id} desconectado")
    
if __name__ == '__main__':
    daemon = Pyro5.Daemon(host='localhost', port=46327)
    
    server = Server(daemon)
    
    uri = daemon.register(server.lobby, objectId="Tic-Tac-Toe")
    
    daemon.validateHandshake = server.client_connected
    daemon.clientDisconnect = server.client_disconnected
    
    print("Ready. Object uri =", uri)
    daemon.requestLoop()