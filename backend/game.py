from backend.user import UserData, User
from functools import wraps
from common.utility import WordType
from backend.generate import WordGenerator


class Game:
    def __init__(self):
        self.user_1_data = UserData()
        self.user_1 = User(self)
        self.user_2_data = UserData()
        self.user_2 = User(self)
        self.registered = 0
        self.initialized = False
        self.generator = WordGenerator()

    def demo_setup(self):
        def get_10_words():
            words = []
            for x in range(10):
                words.append(self.generator.get_word())
            return words

        self.user_1_data.update_words(WordType.ATTACK, get_10_words())
        self.user_1_data.update_words(WordType.DEFEND, get_10_words())
        self.user_2_data.update_words(WordType.ATTACK, get_10_words())
        self.user_2_data.update_words(WordType.DEFEND, get_10_words())

    def _game_started(func):
        @wraps(func)
        def wrapper(inst, *args, **kwargs):
            if not inst.initialized:
                raise Exception('game not started')
            return func(inst, *args, **kwargs)
        return wrapper

    @_game_started
    def type_key(self, user, key):
        caller, _ = self._get_caller(user)
        caller.type_key(key)

    @_game_started
    def remove_previous(self, user):
        caller, _ = self._get_caller(user)
        caller.remove_previous()

    @_game_started
    def publish_word(self, user):
        caller, other = self._get_caller(user)
        word = caller.get_current_word()
        if caller.publish_word():
            other.update_words(WordType.DEFEND, [word])

    @_game_started
    def toggle_mode(self, user):
        caller, _ = self._get_caller(user)
        caller.toggle_mode()

    @_game_started
    def get_data(self, user):
        caller, other = self._get_caller(user)
        payload = {}
        payload[WordType.ATTACK] = list(
            caller.get_words(WordType.ATTACK).queue)
        payload[WordType.DEFEND] = list(
            caller.get_words(WordType.DEFEND).queue)
        payload[WordType.RIVAL] = list(
            other.get_words(WordType.DEFEND).queue)
        payload['mode'] = caller.get_mode()
        payload['current'] = caller.get_current_word()
        return payload

    # the user could be replaced with an interface
    # so it couldn't change its state internally
    def register_user(self):
        if self.initialized:
            raise Exception('game is full')

        if self.registered == 0:
            self.registered += 1
            return self.user_1

        elif self.registered == 1:
            self.registered += 1
            self._start_game()
            return self.user_2

    def _start_game(self):
        self.initialized = True

    def _get_caller(self, caller):
        if caller is self.user_1:
            return self.user_1_data, self.user_2_data
        return self.user_2_data, self.user_1_data
