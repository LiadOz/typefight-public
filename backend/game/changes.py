from common.utility import WordType
from enum import Enum


class ChangeType(Enum):
    ADD_LETTER = 'ADD_LETTER'
    REMOVE_LETTER = 'REMOVE_LETTER'
    ADD_ATTACK = 'ADD_ATTACK'
    ADD_DEFEND = 'ADD_DEFEND'
    REMOVE_ATTACK = 'REMOVE_ATTACK'
    REMOVE_DEFEND = 'REMOVE_DEFEND'
    CLEAR_WORD = 'CLEAR_WORD'
    TOGGLE_MODE = 'TOGGLE_MODE'


class PlayerChanges:
    def __init__(self):
        self.changes = []
        self.fetchers = []

    def _add_change(self, c_type, data):
        for fetcher in self.fetchers:
            fetcher.add_change((c_type, data))
        # self.changes.append((c_type, data))

    def add_letter(self, letter):
        self._add_change(ChangeType.ADD_LETTER, letter)

    def remove_letter(self):
        self._add_change(ChangeType.REMOVE_LETTER, '')

    def add_word(self, w_type, word):
        c_type = None
        if w_type is WordType.ATTACK:
            c_type = ChangeType.ADD_ATTACK
        if w_type is WordType.DEFEND:
            c_type = ChangeType.ADD_DEFEND
        self._add_change(c_type, word)

    def remove_word(self, w_type, word):
        c_type = None
        if w_type is WordType.ATTACK:
            c_type = ChangeType.REMOVE_ATTACK
        if w_type is WordType.DEFEND:
            c_type = ChangeType.REMOVE_DEFEND
        self._add_change(c_type, word)

    def clear_word(self):
        self._add_change(ChangeType.CLEAR_WORD, '')

    def add_fecther(self, fetcher):
        self.fetchers.append(fetcher)

    def flush_changes(self):
        self.changes = []


class ChangeFetcher:
    def __init__(self, keyword):
        self.keyword = keyword
        self.data = []

    def add_change(self, change):
        self.data.append(change)

    def fetch_all(self, format=False):
        change_list = []
        for x, y in self.data:
            if format:
                change_list.append((x.value, y))
            else:
                change_list.append((x, y))
        payload = {self.keyword: change_list}
        self.data = []
        return payload
