from enum import Enum


class WordType(Enum):
    ATTACK = 'ATTACK'
    DEFEND = 'DEFEND'


class Word:
    def __init__(self):
        self.letters = []

    def add_letter(self, letter):
        if len(letter) > 1:
            raise Exception(f'Not a letter {letter}')
        self.letters.append(letter)

    def remove_letter(self):
        if self.letters:
            self.letters.pop()

    def set_word(self, text):
        self.letters = text.split('')

    def reset_word(self):
        self.letters = []

    def get_text(self):
        return ''.join(self.letters)
