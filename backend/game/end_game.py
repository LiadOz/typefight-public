from backend.game.grid import Grid
from enum import Enum


class EnderType(Enum):
    GRID_LINE_ENDER = 'GRID_LINE_ENDER'
    GRID_ACCURACY_ENDER = 'GRID_ACCURACY_ENDER'
    NO_END = 'NO_END'


class EndStatus(Enum):
    NO_END = 'NO_END'
    WIN = 'WIN'
    LOSE = 'LOSE'



def ender_factory(ender_type):
    if ender_type == EnderType.GRID_LINE_ENDER:
        return GridLineEnder
    elif ender_type == EnderType.NO_END:
        return GameEnder
    raise RuntimeError(f'{ender_type} ender not found')


class EndNotify:
    def __init__(self, callback_function):
        self.callback = callback_function

    def notify(self, *args, **kwargs):
        self.callback(*args, **kwargs)


class GameEnder:
    # not to be confused with Enders Game
    def __init__(self, container):
        self.ended = False
        self.end_status = EndStatus.NO_END
        self.container = container

    def set_notifier(self, notifier):
        self.notifier = notifier

    def game_ended(self):
        process_data()
        return self.ended

    # process container data 
    def process_data(self):
        pass

    def notify(self):
        if self.notifier:
            self.notifier.notify((self.ended, self.end_status))


class GridLineEnder(GameEnder):
    # finishes the game when Grid reaches it's final line
    def __init__(self, container):
        super().__init__(container)

    def process_data(self):
        if self.container.get_status():
            self.ended = True
            self.end_status = EndStatus.LOSE
            self.notify()
