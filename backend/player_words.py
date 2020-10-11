from common.utility import WordType
from queue import Queue
import enum


class PlayerWords:
    def __init__(self, attack_container, defend_container):
        self.attack = attack_container()
        self.defend = defend_container()
        self.formatter = WordsFormatter(self)

    def add_word(self, w_type, word):
        self.get_container(w_type).add(word)
        return True

    def remove_word(self, w_type, word):
        self.get_container(w_type).remove(word)
        return True

    def format(self):
        return self.formatter.format()

    def get_container(self, w_type):
        if w_type is WordType.ATTACK:
            return self.attack
        if w_type is WordType.DEFEND:
            return self.defend
        raise ValueError(f'Invalid word type: {w_type}')


class WordsContainer:
    def __init__(self):
        self.container = None

    def add(self, word):
        pass

    def remove(self, word):
        pass

    def get_data(self):
        pass


def create_player_words(words_type):
    if words_type is PlayerWordsType.QUEUE:
        return PlayerWords(WordQueue, WordQueue)
    if words_type is PlayerWordsType.SET:
        return PlayerWords(WordSet, WordSet)


class PlayerWordsType(enum.Enum):
    QUEUE = 'queue'
    SET = 'set'


class WordQueue(WordsContainer):
    def __init__(self):
        self.container = Queue()

    def add(self, word):
        self.container.put(word)

    def remove(self, word):
        # ignores the word and pops
        self.container.get()

    def get_data(self):
        return list(self.container.queue)


class WordSet(WordsContainer):
    def __init__(self):
        self.container = set()

    def add(self, word):
        self.container.add(word)

    def remove(self, word):
        # ignores the word and pops
        self.container.remove(word)

    def get_data(self):
        return self.container.copy()


class WordsFormatter:
    CURRENT_WORD = 'CURRENT'

    def __init__(self, player):
        self.player = player

    def format(self):
        payload = {}
        payload[WordType.ATTACK] = self.player.get_container(
            WordType.ATTACK).get_data()
        payload[WordType.DEFEND] = self.player.get_container(
            WordType.DEFEND).get_data()
        return payload
