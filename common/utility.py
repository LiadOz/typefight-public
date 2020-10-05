import enum


class UserMode(enum.Enum):
    ATTACK = 'ATTACK'
    DEFEND = 'DEFEND'


class WordType(enum.Enum):
    ATTACK = 'ATTACK'
    DEFEND = 'DEFEND'
    RIVAL = 'RIVAL'


class Word:
    def __init__(self):
        self.letters = []

    def add_letter(self, letter):
        self.letters.append(letter)

    def remove_letter(self):
        if self.letters:
            self.letters.pop()

    def get_text(self):
        return ''.join(self.letters)


class Change(enum.Enum):
    ADD = 'ADD'
    REMOVE = 'REMOVE'
    CHANGE = 'CHANGE'
