from backend.game.words import WordsContainer


class Grid(WordsContainer):
    def __init__(self):
        self.word_to_line = {}
        self.lines = []

    def add(self, word):
        top_line = self._top_line()

        ret = top_line.try_add_word(word)
        if not ret:
            self.lines.append(Line())
            self.add(word)
        else:
            self.word_to_line[word] = top_line

        if not top_line.can_add():
            return top_line.get_line()
        return ''

    def remove(self, word):
        # game logic for what's allowed to remove should be in here
        line = self.word_to_line[word]
        line.remove_word(word)
        # if line.empty():
        #     self.lines.remove(line)

    def _top_line(self):
        if not self.lines:
            self.lines.append(Line())
        return self.lines[-1]

    def get_words(self):
        return list(self.word_to_line)

    def get_data(self):
        return [line.get_line() for line in self.lines if not line.can_add()]


class Line:
    SIZE = 25

    def __init__(self):
        self.closed = False
        self.cells = CellArray(self.SIZE)
        self.inserter = WordInserterSimple(self.cells)
        self.words = []

    def _close_line(self):
        self.inserter.insert_words()
        self.closed = True

    def can_add(self):
        if self.closed:
            return False
        return True

    # Tries to add a word, if it cannot be added False is returned
    def try_add_word(self, word):
        ret = self.inserter.add_word(word)
        if not ret:
            self._close_line()
            return False
        self.words.append(word)
        return True

    def remove_word(self, word):
        if not self.closed:
            raise Exception('Cannot remove from open Line')
        self.cells.remove_word(word)

    def get_line(self):
        return self.cells.line_rep()


# determines how to insert words in cells
class WordInserter:
    SEP = '#'

    def __init__(self, cells):
        self.cells = cells
        self.words = []
        self.occupied = 0

    def insert_words(self):
        pass

    # returns False if word is not able to be added
    def add_word(self, word):
        sep = 0
        if self.words:
            sep = 1
        if self.cells.letter_capacity() < len(word) + sep + self.occupied:
            return False
        self.occupied += sep + len(word)
        self.words.append(word)
        return True


# inserts words until there is no more space left
# puts SEP after the first word to fill line
class WordInserterSimple(WordInserter):
    def insert_words(self):
        first = True
        chars = len(self.words) - 1  # The number of spaces needed
        for word in self.words:
            chars += len(word)
        extra_spaces = self.cells.letter_capacity() - chars

        for i, word in enumerate(self.words):
            self.cells.add_word(word)
            if first:
                first = False
                for _ in range(extra_spaces):
                    self.cells.add_char(self.SEP)
            if i < len(self.words) - 1:  # don't put SEP after last word
                self.cells.add_char(self.SEP)


class CellArray:
    def __init__(self, size):
        self.cells = [Cell() for _ in range(size)]
        self.word_to_cells = {}
        self.it = 0

    def letter_capacity(self):
        return len(self.cells)

    def line_rep(self):
        chars = []
        for c in self.cells:
            chars.append(c.get_char())
        return ''.join(chars)

    def add_word(self, word):
        locations = []
        for c in word:
            loc = self.add_char(c)
            locations.append(loc)
        self.word_to_cells[word] = locations

    def remove_word(self, word):
        for loc in self.word_to_cells[word]:
            self.cells[loc].remove_char()

    def add_char(self, char):
        self.cells[self.it].set_char(char)
        index = self.it
        self.it += 1
        return index


class Cell:
    def __init__(self):
        self.char = ''

    def set_char(self, char):
        self.char = char

    def get_char(self):
        return self.char

    def remove_char(self):
        self.char = ''
