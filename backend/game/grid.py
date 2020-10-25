from backend.game.words import WordsContainer


class GridContainer(WordsContainer):
    def __init__(self):
        self.grid = Grid()

    def add(self, word):
        return self.grid.add_word(word)

    def remove(self, word):
        self.grid.remove_word(word)

    def get_words(self):
        # returns grid words
        return self.grid.get_words()

    def accessible_words(self):
        return self.grid.accessible_words()

    def get_data(self):
        # returns grid layout
        return self.grid.get_data()


class Grid:
    LINE_WIDTH = 40

    def __init__(self):
        self.word_to_line = {}
        self.cells = []
        self.lines = []
        self.available_lines = 0

    def add_word(self, word):
        # adds a word to the grid
        top_line = self._top_line()

        ret = top_line.try_add_word(word)
        if not ret:
            self.create_line()
            self.add_word(word)
        else:
            self.word_to_line[word] = top_line

        if not top_line.can_add():
            self.available_lines += 1
            self._update_accessible()
            return top_line.get_line()
        return ''

    def remove_word(self, word):
        line = self.word_to_line[word]
        line.remove_word(word)
        self._update_accessible()

    def create_line(self):
        line = [Cell() for _ in range(Grid.LINE_WIDTH)]
        self.cells.append(line)
        self.lines.append(Line(line))

    def _top_line(self):
        if not self.lines:
            self.create_line()
            self._init_accessible()
        return self.lines[-1]

    def _init_accessible(self):
        for cell in self.cells[0]:
            cell.set_visibility(True)

    def _update_accessible(self):
        if not self.lines:
            return

        # go through all unblocked cells and makes the next blocked visible
        for col in range(Grid.LINE_WIDTH):
            for row in range(self.available_lines):
                if self.cells[row][col].blocked:
                    self.cells[row][col].set_visibility(True)
                    break

    def _print_accessible(self):
        for line in self.cells:
            li1 = []
            li2 = []
            li3 = []
            for cell in line:
                if cell.char:
                    li1.append(cell.char)
                else:
                    li1.append(' ')
                if cell.visible:
                    li2.append('V')
                else:
                    li2.append('X')
                if cell.blocked:
                    li3.append('B')
                else:
                    li3.append('U')
            print(''.join(li1))
            print(''.join(li2))
            print(''.join(li3))
        print()

    def get_words(self):
        return list(self.word_to_line)

    def accessible_words(self):
        acc = set()
        for line in self.lines:
            if line.can_add():
                break
            acc.update(line.get_visible_words())
        return acc

    def get_data(self):
        return [line.get_line() for line in self.lines if not line.can_add()]


class Line:
    def __init__(self, cells):
        self.closed = False
        self.cells = CellArray(cells)
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

    def get_visible_words(self):
        return self.cells.visible_words()


# determines how to insert words in cells
class WordInserter:
    SEP = '#'

    def __init__(self, cells):
        self.cells = cells
        self.words = []
        self.occupied = 0

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
                    self.cells.add_char(self.SEP, block=False)
            if i < len(self.words) - 1:  # don't put SEP after last word
                self.cells.add_char(self.SEP, block=False)


class CellArray:
    def __init__(self, cells):
        self.cells = cells
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
            self.cells[loc].unblock()

    def add_char(self, char, block=True):
        self.cells[self.it].set_char(char)
        if not block:
            self.cells[self.it].unblock()
        index = self.it
        self.it += 1
        return index

    def visible_words(self):
        # find all the words that are visible
        visible = []
        for word, locations in self.word_to_cells.items():
            all_vis = True
            for loc in locations:
                if not self.cells[loc].visible:
                    all_vis = False
                    break
            if all_vis:
                visible.append(word)
        return visible


class Cell:
    def __init__(self):
        self.char = ''
        self.visible = False
        self.blocked = True

    def set_char(self, char):
        self.char = char

    def set_visibility(self, vis):
        self.visible = vis

    def unblock(self):
        self.blocked = False

    def get_char(self):
        return self.char

    def remove_char(self):
        self.char = ''
