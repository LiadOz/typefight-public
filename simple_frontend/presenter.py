from model import Model
from view import View
from utility import WordType
import sys


class Presenter:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

        self.view.render.add_word(WordType.ATTACK, 'attack')
        self.view.render.add_word(WordType.DEFEND, 'defend')
        self.view.render.set_player_message('hell')

    def run(self):
        self.view.run()

    def send_letter(self, event):
        print(event.char)

    def remove_letter(self, event=None):
        pass

    def publish_current_word(self, event=None):
        pass

    def switch_user(self):
        pass


if __name__ == '__main__':
    sys.path.append('../backend')
    app = Presenter()
    app.run()
