from src.TicTac import TicTac
import Pyro5.server as Pyro5

@Pyro5.expose
class Lobby:
    def __init__(self, daemon: Pyro5.Daemon) -> None:
        self.waiting_room = []
        self.lobby = []
        self.uris = []
        self.daemon = daemon
        
    def get_waiting_room(self) -> list:
        return self.waiting_room
    
    def add_to_waiting_room(self, client_id: str) -> None:
        if client_id not in self.waiting_room:
            self.waiting_room.append(client_id)
        return None
    
    def remove_from_waiting_room(self, client_id: str) -> None:
        if client_id in self.waiting_room:
            self.waiting_room.remove(client_id)
        return None
        
    def get_lobby(self) -> list:
        for i, game in enumerate(self.lobby):
            if game.check_win():
                self.lobby.remove(game)
                self.daemon.unregister(self.uris[i])
                self.uris.remove(self.uris[i])
        return self.lobby
    
    def get_game(self, client_id: str) -> None:
        for i, game in enumerate(self.lobby):
            if client_id in game.get_player():
                return self.uris[i]
        return None
    
    def match_players(self, actual_id, target_id: str) -> bool:
        if target_id in self.waiting_room:
            self.waiting_room.remove(target_id)
            game = TicTac(target_id, actual_id)
            uri = self.daemon.register(game, objectId=target_id)
            self.lobby.append(game)
            self.uris.append(uri)
            return True
        else:
            return False