import random


class WordGenerator:
    def __init__(self):
        self.words = []
        with open('backend/words.txt', 'r') as f:
            for line in f:
                self.words.append(line.strip())
        random.shuffle(self.words)

    def get_word(self):
        word = self.words.pop()
        return word
