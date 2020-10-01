import enum


class UserMode(enum.Enum):
    ATTACK = 1
    DEFEND = 2


class WordType(enum.Enum):
    ATTACK = 1
    DEFEND = 2
    RIVAL = 3


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
