from backend.game.words import WordsContainer


class Grid(WordsContainer):
    def __init__(self):
        self.word_to_line = {}
        self.lines = []

    def add(self, word):
        if not self.lines:
            self.lines.append(Line())
        top_line = self.lines[-1]

        top_line.add_word(word)
        self.word_to_line[word] = top_line
        if not top_line.can_add():
            self.lines.append(Line())
            return top_line.get_words()
        return ''

    def remove(self, word):
        # game logic for what's allowed to remove should be in here
        line = self.word_to_line[word]
        line.remove_word(word)
        if line.empty():
            self.lines.remove(line)

    def get_words(self):
        return list(self.word_to_line)

    def get_data(self):
        return [line.get_words() for line in self.lines if not line.can_add()]


class Line:
    CAPACITY = 25

    def __init__(self):
        self.closed = False
        self.words = []
        self.char_count = 0

    def can_add(self):
        if self.closed:
            return False
        return True

    def add_word(self, word):
        if not self.can_add():
            raise Exception('Too many charaters in line')
        self.words.append(word)
        self.char_count += len(word)
        if self.char_count >= Line.CAPACITY:
            self.closed = True

    def remove_word(self, word):
        # it is assumed that the word exists
        self.words.remove(word)

    def get_words(self):
        return self.words.copy()

    def empty(self):
        if self.words:
            return False
        return True
