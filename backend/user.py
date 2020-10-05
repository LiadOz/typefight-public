import queue
from collections import defaultdict
from common.utility import UserMode, WordType, Word, Change
from functools import wraps


class UserData:
    def __init__(self):
        self.current_word = Word()
        self.defend = queue.Queue()
        self.attack = queue.Queue()
        self.mode = UserMode.DEFEND
        self.queue = self.defend

    def get_data(self):
        payload = {}
        payload[WordType.ATTACK.value] = list(
            self.get_words(WordType.ATTACK).queue)
        payload[WordType.DEFEND.value] = list(
            self.get_words(WordType.DEFEND).queue)
        payload['MODE'] = self.get_mode().value
        payload['CURRENT'] = self.get_current_word()
        return payload

    def update_words(self, word_type, words):
        add_queue = self._get_queue(word_type)
        for word in words:
            add_queue.put(word)

    # this is not copied so it can be changed
    def get_words(self, word_type):
        return self._get_queue(word_type)

    def get_mode(self):
        return self.mode

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

    def _get_queue(self, word_type):
        add_queue = None
        if word_type == WordType.ATTACK:
            add_queue = self.attack
        else:
            add_queue = self.defend
        return add_queue


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
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(dict))

    def fetch(self):
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
        if index == 1:
            return self.user_2.interface
        elif index == 0:
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
        self._get_player(user).type_key(key)
        self._update_user(user)

    @_game_started
    def remove_previous(self, user):
        self._get_player(user).remove_previous()
        self._update_user(user)

    @_game_started
    def publish_word(self, user):
        caller, other = self._get_player(user), self._get_rival(user)
        word = caller.get_current_word()
        ret = caller.publish_word()
        if ret == UserMode.ATTACK:
            other.update_words(WordType.DEFEND, [word])

        if ret:  # if something changed update both users
            if user is self.user_1.interface:
                self._update_user(self.user_2.interface)
            elif user is self.user_2.interface:
                self._update_user(self.user_1.interface)
            self._update_user(user)

    @_game_started
    def toggle_mode(self, user):
        self._get_player(user).toggle_mode()

    @_game_started
    def get_data(self, user):
        payload = self._get_player(user).get_data()
        payload[WordType.RIVAL.value] = list(
            self._get_rival(user).get_words(WordType.DEFEND).queue)
        return payload

    def set_broadcast(self, func):
        self.send_data = func

    def _get_player(self, user):
        if user is self.user_1.interface:
            return self.user_1.data
        elif user is self.user_2.interface:
            return self.user_2.data
        raise Exception('No player found')

    def _get_rival(self, user):
        if user is self.user_1.interface:
            return self.user_2.data
        elif user is self.user_2.interface:
            return self.user_1.data
        raise Exception('No rival found')

    def _user_id(self, user):
        if user is self.user_1.interface:
            return '1'
        elif user is self.user_2.interface:
            return '2'

    def _update_user(self, user):
        self.send_data(self._user_id(user), self.get_data(user))
