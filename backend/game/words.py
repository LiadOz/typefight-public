from common.utility import WordType
from queue import Queue


class WordsContainer:
    def __init__(self):
        self.container = None

    def add(self, word):
        pass

    def remove(self, word):
        pass

    def get_data(self):
        pass

    def get_status(self):
        pass


class WordQueue(WordsContainer):
    def __init__(self):
        self.container = Queue()

    def add(self, word):
        self.container.put(word)
        return word

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
        return word

    def remove(self, word):
        self.container.remove(word)

    def get_data(self):
        return list(self.container)


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
        payload[self.CURRENT_WORD] = self.player.current_word.get_text()
        return payload


class WordsFormatterQueue(WordsFormatter):
    MODE = 'MODE'

    def format(self):
        payload = super().format()
        payload[WordsFormatterQueue.MODE] = self.player.mode
        return payload
