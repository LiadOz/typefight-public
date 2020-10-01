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
