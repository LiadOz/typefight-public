from backend.user import UsersManager
from backend.generate import WordGenerator
from common.utility import WordType


class Game:
    def __init__(self):
        self.manager = UsersManager()
        self.registered = 0
        self.initialized = False
        self.generator = WordGenerator()

    def demo_setup(self):
        def get_10_words():
            words = []
            for x in range(10):
                words.append(self.generator.get_word())
            return words

        self.manager.user_1.data.update_words(WordType.ATTACK, get_10_words())
        self.manager.user_1.data.update_words(WordType.DEFEND, get_10_words())
        self.manager.user_2.data.update_words(WordType.ATTACK, get_10_words())
        self.manager.user_2.data.update_words(WordType.DEFEND, get_10_words())

    # the user could be replaced with an interface
    # so it couldn't change its state internally
    def register_user(self):
        if self.registered == 2:
            raise Exception('game is full')

        user = self.manager.get_user(self.registered)
        self.registered += 1
        if self.registered == 2:
            self._start_game()
        return user

    def set_broadcast(self, func):
        self.manager.set_broadcast(func)

    def _start_game(self):
        self.manager.start_game()
        self.initialized = True
