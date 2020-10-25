from backend.game.players import Player
from backend.game.data import PlayerDataType
from common.utility import WordType
from threading import Thread
from time import sleep
from random import uniform, choice


class BotPlayer(Player):
    def __init__(self, u_id, data_type):
        super().__init__(u_id, data_type)
        self.set_speed(80)

    def set_speed(self, wpm):
        self.seconds = 60 / (wpm * 5)

    def pause(self):
        sleep(self.seconds)

    def type_word(self, word):
        for c in word:
            self.type_key(c)
            self.pause()

    def _run(self):
        word = self._get_next_word()
        while word:
            self.type_word(word)
            self.publish_word()
            self.pause()
            word = self._get_next_word()

    def start_playing(self):
        Thread(target=self._run).start()


class QueueBot(BotPlayer):
    def __init__(self, u_id):
        super().__init__(u_id, PlayerDataType.QUEUE)

    def _get_next_word(self):
        candidates = self.get_publishable()
        self.toggle_mode()
        current = candidates[self.get_mode()]
        if current:
            return current
        self.toggle_mode()
        current = candidates[self.get_mode()]
        if current:
            return current
        else:
            return ''


class GridBot(BotPlayer):
    DEFEND_CHANCE = 0.17

    def __init__(self, u_id):
        super().__init__(u_id, PlayerDataType.GRID)

    def _choose_mode(self):
        if uniform(0, 1) < GridBot.DEFEND_CHANCE:
            return WordType.DEFEND
        return WordType.ATTACK

    def _get_next_word(self):
        candidates = self.get_publishable()
        mode = self._choose_mode()
        words = list(candidates[mode])
        if words:
            return choice(words)

        # in case no word was selected
        if mode is WordType.ATTACK:
            mode = WordType.DEFEND
        if mode is WordType.DEFEND:
            mode = WordType.ATTACK
        words = list(candidates[mode])
        if words:
            return choice(words)
        return ''
