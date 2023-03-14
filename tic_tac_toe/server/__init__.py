import Pyro5.server as Pyro5
from src.TicTac import TicTac

class Server:
    def __init__(self) -> None:
        self._client_id_by_connection = {}
        self.game = TicTac()

    def client_connected(self, connection: Pyro5, client_id: str) -> None:
        print(f"Cliente: {client_id} conectado")
        self.game.set_player(client_id)

        self._client_id_by_connection[connection] = client_id

    def client_disconnected(self, connection: Pyro5) -> None:
        client_id = self._client_id_by_connection[connection]
        self.game.reset_board()
        print(f"Cliente: {client_id} desconectado")
    
if __name__ == '__main__':
    server = Server()
    
    daemon = Pyro5.Daemon(port=46327)
    uri = daemon.register(server.game, objectId="Tic-Tac-Toe")
    
    daemon.validateHandshake = server.client_connected
    daemon.clientDisconnect = server.client_disconnected
    
    print("Ready. Object uri =", uri)
    daemon.requestLoop()