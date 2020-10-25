from backend.game.data import create_player_data, PlayerDataType
from common.utility import WordType


class IPlayer:
    def __init__(self, u_id, player_data_type):
        self.u_id = u_id
        self.player_data_type = player_data_type

    def attach_executor(self, executor):
        self.executor = executor
        executor.register_player(self.u_id,
                                 create_player_data(self.player_data_type))


class Player(IPlayer):
    def __init__(self, u_id, player_data_type):
        super().__init__(u_id, player_data_type)

    def type_key(self, key):
        self.executor.type_key(self.u_id, key)

    def remove_previous(self):
        self.executor.remove_key(self.u_id)

    def add_word(self, w_type, word):
        self.executor.add_word(self.u_id, w_type, word)

    def remove_word(self, w_type, word):
        self.executor.remove_word(self.u_id, w_type, word)

    def publish_word(self):
        self.executor.publish_word(self.u_id)

    def toggle_mode(self):
        self.executor.toggle_mode(self.u_id)

    def get_data(self):
        return self.executor.player_data(self.u_id)

    def get_my_data(self):
        return self.executor.get_my_data(self.u_id)

    def get_mode(self):
        return self.executor.get_mode(self.u_id)

    def get_publishable(self):
        return self.executor.get_publishable(self.u_id)

    def formatted_data(self):
        payload = self.get_data()
        new_payload = {}
        for k, v in payload.items():
            temp = {}
            for i, j in v.items():
                if i in WordType:
                    temp[i.value] = j
                elif j in WordType:
                    temp[i] = j.value
                else:
                    temp[i] = j
            new_payload[k] = temp
        return new_payload


class HumanPlayer(Player):
    def __init__(self, u_id, player_data_type):
        super().__init__(u_id, player_data_type)

    def register_fetchers(self):
        self.my_fetcher, self.other_fetcher = self.executor.create_fetchers(
            self.u_id)

    def get_changes(self):
        payload = self.my_fetcher.fetch_all(format=True)
        payload.update(self.other_fetcher.fetch_all(format=True))
        return payload


class QueuePlayer(HumanPlayer):
    def __init__(self, u_id):
        super().__init__(u_id, PlayerDataType.QUEUE)


class SetPlayer(HumanPlayer):
    def __init__(self, u_id):
        super().__init__(u_id, PlayerDataType.SET)


class GridPlayer(HumanPlayer):
    def __init__(self, u_id):
        super().__init__(u_id, PlayerDataType.GRID)
