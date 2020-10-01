import queue
import enum
from typed import Word


class User:
    def __init__(self):
        self.current_word = Word()
        self.defend = queue.Queue()
        self.attack = queue.Queue()
        self.rival = queue.Queue()
        self.mode = Mode.DEFEND

    def update_words(self, word_type, words):
        add_queue = self._get_queue(word_type)
        for word in words:
            add_queue.put(word)

    # this is not copied so it can be changed
    def get_words(self, word_type):
        return self._get_queue(word_type)

    def _get_queue(self, word_type):
        add_queue = None
        if word_type == WordType.ATTACK:
            add_queue = self.attack
        elif word_type == WordType.DEFEND:
            add_queue = self.defend
        else:
            add_queue = self.rival
        return add_queue

    # this should be only attack or defend
    def toggle_mode(self):
        if self.mode == Mode.ATTACK:
            self.mode = Mode.DEFEND
        else:
            self.mode = Mode.ATTACK
        print(self.mode)

    def type_key(self, key):
        self.current_word.add_letter(key)

    def remove_previous(self):
        self.current_word.remove_letter()

    def get_current_word(self):
        return self.current_word.get_text()

    def publish_word(self):
        print(self.get_current_word(), self.defend.queue[0])
        if self.mode == Mode.ATTACK and \
           self.get_current_word() == self.attack.queue[0]:
            self.attack.get()
            self.current_word = Word()
            return True
        elif self.mode == Mode.DEFEND and \
                self.get_current_word() == self.defend.queue[0]:
            print('inside')
            self.defend.get()
            self.current_word = Word()
            return True


# Manages the active user
# the first user is the default user
class UserManager:
    def __init__(self, user_1, user_2):
        self.user_1 = user_1
        self.user_2 = user_2
        self.active_user_flag = 0
        self.current_user = self.user_1
        self.other_user = self.user_2

    def switch_user(self):
        self.active_user_flag = not self.active_user_flag
        if self.active_user_flag:
            self.current_user = self.user_1
            self.other_user = self.user_2
        else:
            self.current_user = self.user_2
            self.other_user = self.user_1

    def update_words(self, word_type, words):
        return self.current_user.update_words(word_type, words)

    def get_words(self, word_type):
        return self.current_user.get_words(word_type)

    def toggle_mode(self):
        return self.current_user.toggle_mode()

    def type_key(self, key):
        return self.current_user.type_key(key)

    def remove_previous(self):
        return self.current_user.remove_previous()

    def get_current_word(self):
        return self.current_user.get_current_word()

    def publish_word(self):
        return self.current_user.publish_word()


class Mode(enum.Enum):
    ATTACK = 1
    DEFEND = 2


class WordType(enum.Enum):
    ATTACK = 1
    DEFEND = 2
    RIVAL = 3
