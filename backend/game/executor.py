from functools import wraps
from common.utility import WordType
from backend.game.changes import ChangeFetcher
from backend.game.data import GameData
from backend.generate import WordGenerator
from backend.game.end_game import EndNotify
from enum import Enum


class ExecutorType(Enum):
    DUEL = 2
    ROYALE = 100


class GameStatus(Enum):
    INIT = 'INIT'
    ACTIVE = 'ACTIVE'
    ENDED = 'ENDED'


class PlayerStatus(Enum):
    PLAYING = 'PLAYING'
    WINNER = 'Winner'
    LOSER = 'Loser'


def executor_factory(executer_type):
    if executer_type == ExecutorType.DUEL:
        return DuelExecutor()
    elif executer_type == ExecutorType.ROYALE:
        return RoyaleExecutor()

def active_game(func):
    @wraps(func)
    def _active_game(inst, *args, **kwargs):
        if inst.status == GameStatus.ACTIVE:
            ret = func(inst, *args, **kwargs)
            return ret
        else:
            raise RuntimeError('Game not active')
    return _active_game



class Executor:
    def __init__(self):
        self.data = GameData()
        self.word_gen = WordGenerator()
        self.status = GameStatus.INIT
        self.player_status = {}

    def register_user(self, player_id, player_data):
        self.player_status[player_id] = PlayerStatus.PLAYING

    def add_word(self, caller_id, w_type, word):
        self.data.add_word(caller_id, w_type, word)

    def remove_word(self, caller_id, w_type, word):
        self.data.remove_word(caller_id, w_type, word)

    @active_game
    def type_key(self, caller_id, key):
        self.data.type_key(caller_id, key)

    @active_game
    def remove_key(self, caller_id):
        self.data.remove_key(caller_id)

    def publish_word(self, caller_id):
        pass

    def get_publishable(self, caller_id):
        return self.data.get_publishable(caller_id)

    def toggle_mode(self, caller_id):
        self.data.toggle_mode(caller_id)

    def get_mode(self, caller_id):
        return self.data.get_mode(caller_id)

    def init_game(self):
        pass

    def start_game(self):
        self.status = GameStatus.ACTIVE

    def end_game(self):
        self.status = GameStatus.ENDED

    def get_players_status(self):
        return self.player_status


class DuelExecutor(Executor):
    def __init__(self):
        super().__init__()
        self.registered = 0

    def register_user(self, player_id, player_data):
        if self.registered == 0:
            self.player_1 = player_id
            self.data.add_player(player_id, player_data)
        elif self.registered == 1:
            self.player_2 = player_id
            self.data.add_player(player_id, player_data)
        else:
            raise Exception('Only two users allowed in duel')
        super().register_user(player_id, player_data)
        self.data.set_ender(
            player_id, DuelEndNotifier(self._end_callback, player_id))
        self.registered += 1

    def get_opponent(self, caller_id):
        if caller_id == self.player_1:
            return self.player_2
        elif caller_id == self.player_2:
            return self.player_1
        else:
            raise Exception('Unknown caller')

    @active_game
    def publish_word(self, caller_id):
        mode, word = self.data.publish_word(caller_id)
        if word:
            self.add_word(self.get_opponent(caller_id), WordType.DEFEND, word)
            self.add_word(caller_id, WordType.ATTACK, self.word_gen.get_word())

    def get_my_data(self, caller_id):
        return self.data.player_data(caller_id)

    def player_data(self, caller_id):
        payload = {}
        payload['PLAYER'] = self.data.player_data(caller_id)
        payload['RIVAL'] = self.data.player_data(self.get_opponent(caller_id))
        return payload

    def create_fetchers(self, caller_id):
        f1 = ChangeFetcher("PLAYER")
        f2 = ChangeFetcher("RIVAL")
        self.data.add_fetcher(caller_id, f1)
        self.data.add_fetcher(self.get_opponent(caller_id), f2)
        return f1, f2

    def init_game(self):
        for _ in range(10):
            self.add_word(self.player_1, WordType.ATTACK,
                          self.word_gen.get_word())
            self.add_word(self.player_2, WordType.ATTACK,
                          self.word_gen.get_word())
        for _ in range(60):
            self.add_word(self.player_1, WordType.DEFEND,
                          self.word_gen.get_word())
            self.add_word(self.player_2, WordType.DEFEND,
                          self.word_gen.get_word())

    def _end_callback(self, player_id, *args, **kwargs):
        self.player_status[player_id] = PlayerStatus.LOSER
        self.player_status[self.get_opponent(player_id)] = PlayerStatus.WINNER
        self.end_game()


class DuelEndNotifier(EndNotify):
    def __init__(self, callback_function, player_id):
        super().__init__(callback_function)
        self.player_id = player_id

    def notify(self, *args, **kwargs):
        self.callback(self.player_id, *args, **kwargs)


class RoyaleExecutor(Executor):
    pass
