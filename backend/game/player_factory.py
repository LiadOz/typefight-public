from backend.game.bots import BotPlayer
from backend.game.players import QueuePlayer, SetPlayer, HumanPlayer
from enum import Enum


class PlayerType(Enum):
    BOT_QUEUE_PLAYER = 'BOT_QUEUE_PLAYER'
    SET_PLAYER = 'SET_PLAYER'
    QUEUE_PLAYER = 'QUEUE_PLAYER'


def player_factory(player_type):
    if player_type == PlayerType.BOT_QUEUE_PLAYER:
        return BotPlayer
    elif player_type == PlayerType.QUEUE_PLAYER:
        return QueuePlayer
    elif player_type == PlayerType.SET_PLAYER:
        return SetPlayer
    return HumanPlayer
