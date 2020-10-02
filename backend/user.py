import queue
from common.utility import UserMode, WordType, Word
from functools import wraps


class UserData:
    def __init__(self):
        self.current_word = Word()
        self.defend = queue.Queue()
        self.attack = queue.Queue()
        self.mode = UserMode.DEFEND
        self.queue = self.defend

    def update_words(self, word_type, words):
        add_queue = self._get_queue(word_type)
        for word in words:
            add_queue.put(word)

    # this is not copied so it can be changed
    def get_words(self, word_type):
        return self._get_queue(word_type)

    def get_mode(self):
        return self.mode

    def _get_queue(self, word_type):
        add_queue = None
        if word_type == WordType.ATTACK:
            add_queue = self.attack
        else:
            add_queue = self.defend
        return add_queue

    # this should be only attack or defend
    def toggle_mode(self):
        if self.mode == UserMode.ATTACK:
            self.mode = UserMode.DEFEND
            self.queue = self.defend
        else:
            self.mode = UserMode.ATTACK
            self.queue = self.attack
        print(self.mode)

    def type_key(self, key):
        self.current_word.add_letter(key)

    def remove_previous(self):
        self.current_word.remove_letter()

    def get_current_word(self):
        return self.current_word.get_text()

    def publish_word(self):
        q = self.queue
        if not q.empty() and self.get_current_word() == q.queue[0]:
            q.get()
            self.current_word = Word()
            return self.mode
        return False


class User:
    def __init__(self, manager):
        self.manager = manager

    def _write_action(func):
        @wraps(func)
        def wrapper(inst, *args, **kwargs):
            func(inst, *args, **kwargs)
            return inst.get_data()

        return wrapper

    def get_data(self):
        return self.manager.get_data(self)

    @_write_action
    def type_key(self, key):
        self.manager.type_key(self, key)

    @_write_action
    def remove_previous(self):
        self.manager.remove_previous(self)

    @_write_action
    def publish_word(self):
        self.manager.publish_word(self)

    def toggle_mode(self):
        self.manager.toggle_mode(self)


class UserChanges:
    pass


class UserWrapper:
    def __init__(self, manager):
        self.data = UserData()
        self.interface = User(manager)
        self.changes = UserChanges()


# manages the interaction between users
class UsersManager:
    def __init__(self):
        self.user_1 = UserWrapper(self)
        self.user_2 = UserWrapper(self)
        self.initialized = False

    def get_user(self, index):
        if index:
            return self.user_2.interface
        else:
            return self.user_1.interface

    def start_game(self):
        self.initialized = True

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
        if caller.publish_word() == UserMode.ATTACK:
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
        payload[WordType.RIVAL] = list(other.get_words(WordType.DEFEND).queue)
        payload['mode'] = caller.get_mode()
        payload['current'] = caller.get_current_word()
        return payload

    def _get_caller(self, caller):
        if caller is self.user_1.interface:
            return self.user_1.data, self.user_2.data
        return self.user_2.data, self.user_1.data
