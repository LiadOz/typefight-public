from common.utility import WordType, Word
from backend.game.changes import PlayerChanges
from backend.game.words import (WordQueue, WordsFormatter, WordSet,
                                WordsFormatterQueue)
from backend.game.grid import GridContainer
from backend.game.end_game import EnderType, ender_factory
from enum import Enum


class GameData:
    def __init__(self):
        self.mapping = {}

    def add_player(self, caller_id, player_data):
        self.mapping[caller_id] = player_data

    def add_word(self, caller_id, w_type, word):
        self.mapping[caller_id].add_word(w_type, word)

    def remove_word(self, caller_id, w_type, word):
        self.mapping[caller_id].remove_word(w_type, word)

    def type_key(self, caller_id, key):
        self.mapping[caller_id].type_key(key)

    def remove_key(self, caller_id):
        self.mapping[caller_id].remove_key()

    def publish_word(self, caller_id):
        return self.mapping[caller_id].publish_word()

    def get_publishable(self, caller_id):
        return self.mapping[caller_id].get_publishable()

    def toggle_mode(self, caller_id):
        self.mapping[caller_id].toggle_mode()

    def player_data(self, caller_id):
        return self.mapping[caller_id].format()

    def get_mode(self, caller_id):
        return self.mapping[caller_id].get_mode()

    def fetch_changes(self, caller_id, fetcher):
        return self.mapping[caller_id].fetch_changes(fetcher)

    def add_fetcher(self, caller_id, fetcher):
        return self.mapping[caller_id].add_fetcher(fetcher)

    def set_ender(self, caller_id, notifier):
        return self.mapping[caller_id].get_ender().set_notifier(notifier)


class PlayerData:
    def __init__(self, attack_container, defend_container,
                 formatter, ender_type):
        self.attack = attack_container()
        self.defend = defend_container()
        self.current_word = Word()
        self.formatter = formatter(self)
        self.changes = PlayerChanges()
        self.ender = ender_factory(ender_type)(self.defend)

    def get_ender(self):
        return self.ender

    def add_word(self, w_type, word):
        details = self.get_container(w_type).add(word)
        self.changes.add_word(w_type, details)
        self.ender.process_data()
        return True

    def remove_word(self, w_type, word):
        self.get_container(w_type).remove(word)
        self.changes.remove_word(w_type, word)
        self.ender.process_data()
        return True

    def type_key(self, key):
        self.current_word.add_letter(key)
        self.changes.add_letter(key)

    def remove_key(self):
        self.current_word.remove_letter()
        self.changes.remove_letter()

    def publish_word(self):
        pass

    def get_publishable(self):
        pass

    def fetch_changes(self, fetcher):
        self.changes.fetch_changes(fetcher)

    def add_fetcher(self, fetcher):
        self.changes.add_fecther(fetcher)

    def format(self):
        return self.formatter.format()

    def get_container(self, w_type):
        if w_type is WordType.ATTACK:
            return self.attack
        if w_type is WordType.DEFEND:
            return self.defend
        raise ValueError(f'Invalid word type: {w_type}')


class PlayerDataQueue(PlayerData):
    def __init__(self):
        super().__init__(WordQueue, WordQueue, WordsFormatterQueue,
                         EnderType.NO_END)
        self.mode = WordType.DEFEND

    def publish_word(self):
        """
        tries to publish a word if it was in attack mode it returns the word
        """
        word = self.get_publishable()[self.mode]
        li = self.get_container(self.mode).get_data()
        if word and word == self.current_word.get_text():
            word = li[0]
            self.remove_word(self.mode, word)
            self.current_word.reset_word()
            self.changes.clear_word()
            if self.mode == WordType.ATTACK:
                return self.mode, word
        return self.mode, ''

    def toggle_mode(self):
        if self.mode == WordType.ATTACK:
            self.mode = WordType.DEFEND
        else:
            self.mode = WordType.ATTACK

    def get_publishable(self):
        payload = {}
        for w_type in WordType:
            container = self.get_container(w_type).get_data()
            data = ''
            if container:
                data = container[0]
            payload[w_type] = data
        return payload

    def get_mode(self):
        return self.mode

    def format(self):
        return self.formatter.format()


class PlayerDataSet(PlayerData):
    def __init__(self):
        super().__init__(WordSet, WordSet, WordsFormatter, EnderType.NO_END)
        self.mode = WordType.DEFEND

    def publish_word(self):
        current = self.current_word.get_text()
        mode, ret = None, ''
        if current in self.get_container(WordType.ATTACK).get_data():
            mode = WordType.ATTACK
            ret = current
        elif current in self.get_container(WordType.DEFEND).get_data():
            mode = WordType.DEFEND
        if mode:
            self.remove_word(mode, current)
            self.current_word.reset_word()
            self.changes.clear_word()
        return mode, ret

    def get_publishable(self):
        payload = {}
        for w_type in WordType:
            payload[w_type] = self.get_container(w_type).get_data()
        return payload

    def format(self):
        return self.formatter.format()


class PlayerDataGrid(PlayerData):
    def __init__(self):
        super().__init__(WordSet, GridContainer, WordsFormatter,
                         EnderType.GRID_LINE_ENDER)
        self.mode = WordType.DEFEND

    def publish_word(self):
        current = self.current_word.get_text()
        mode, ret = None, ''
        candidates = self.get_publishable()
        if current in candidates[WordType.ATTACK]:
            mode = WordType.ATTACK
            ret = current
        elif current in candidates[WordType.DEFEND]:
            mode = WordType.DEFEND
        if mode:
            self.remove_word(mode, current)
            self.current_word.reset_word()
            self.changes.clear_word()
        return mode, ret

    def get_publishable(self):
        payload = {}
        payload[WordType.ATTACK] = \
            self.get_container(WordType.ATTACK).get_data()
        payload[WordType.DEFEND] = \
            self.get_container(WordType.DEFEND).accessible_words()
        return payload


class PlayerDataType(Enum):
    QUEUE = 'queue'
    SET = 'set'
    GRID = 'grid'


def create_player_data(data_type):
    if data_type is PlayerDataType.QUEUE:
        return PlayerDataQueue()
    if data_type is PlayerDataType.SET:
        return PlayerDataSet()
    if data_type is PlayerDataType.GRID:
        return PlayerDataGrid()
