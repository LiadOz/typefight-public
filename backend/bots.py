from backend.players import QueuePlayer
from threading import Thread
from time import sleep


class BotPlayer(QueuePlayer):
    def __init__(self, executor, u_id):
        super().__init__(executor, u_id)
        self.set_speed(50)

    def set_speed(self, wpm):
        self.seconds = 60 / (wpm * 5)

    def pause(self):
        sleep(self.seconds)

    def get_next_word(self):
        self.toggle_mode()
        current = self.get_my_data()[self.get_mode()]
        if current:
            return current[0]
        else:
            return ''

    def type_word(self, word):
        for c in word:
            self.type_key(c)
            self.pause()

    def _run(self):
        word = self.get_next_word()
        while word:
            self.type_word(word)
            self.publish_word()
            word = self.get_next_word()

    def start_playing(self):
        Thread(target=self._run).start()
