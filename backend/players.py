from common.utility import WordType
from backend.player_words import create_player_data, GameData, PlayerDataType


def executor_factory(count):
    if count == 1:
        return None
    if count == 2:
        return DuelExecutor()
    else:
        return RoyaleExecutor()


class Executor:
    def __init__(self):
        self.data = GameData()

    def register_user(self, player_id, player_data):
        pass

    def add_word(self, caller_id, w_type, word):
        self.data.add_word(caller_id, w_type, word)

    def remove_word(self, caller_id, w_type, word):
        self.data.remove_word(caller_id, w_type, word)

    def type_key(self, caller_id, key):
        self.data.type_key(caller_id, key)

    def remove_key(self, caller_id):
        self.data.remove_key(caller_id)

    def publish_word(self, caller_id):
        pass

    def toggle_mode(self, caller_id):
        self.data.toggle_mode(caller_id)

    def get_mode(self, caller_id):
        return self.data.get_mode(caller_id)


class DuelExecutor(Executor):
    def __init__(self):
        super().__init__()
        self.registered = 0

    def register_player(self, player_id, player_data):
        if self.registered == 0:
            self.player_1 = player_id
            self.data.add_player(player_id, player_data)
        elif self.registered == 1:
            self.player_2 = player_id
            self.data.add_player(player_id, player_data)
        else:
            raise Exception('Only two users allowed in duel')
        self.registered += 1

    def get_opponent(self, caller_id):
        if caller_id == self.player_1:
            return self.player_2
        elif caller_id == self.player_2:
            return self.player_1
        else:
            raise Exception('Unknown caller')

    def publish_word(self, caller_id):
        word = self.data.publish_word(caller_id)
        if word:
            self.data.add_word(
                self.get_opponent(caller_id), WordType.DEFEND, word)

    def get_my_data(self, caller_id):
        return self.data.player_data(caller_id)

    def player_data(self, caller_id):
        payload = {}
        payload['PLAYER'] = self.data.player_data(caller_id)
        payload['RIVAL'] = self.data.player_data(self.get_opponent(caller_id))
        return payload


class RoyaleExecutor(Executor):
    pass


class IPlayer:
    def __init__(self, executor, u_id, player_data_type):
        self.u_id = u_id
        self.executor = executor
        self.executor.register_player(u_id,
                                      create_player_data(player_data_type))


class Player(IPlayer):
    def __init__(self, executor, u_id, player_data_type):
        super().__init__(executor, u_id, player_data_type)

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


class QueuePlayer(Player):
    def __init__(self, executor, u_id):
        super().__init__(executor, u_id, PlayerDataType.QUEUE)
