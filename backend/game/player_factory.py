from backend.game.bots import QueueBot, GridBot
from backend.game.players import (QueuePlayer, SetPlayer, HumanPlayer,
                                  GridPlayer)
from enum import Enum


class PlayerType(Enum):
    BOT_QUEUE_PLAYER = 'BOT_QUEUE_PLAYER'
    BOT_GRID_PLAYER = 'BOT_GRID_PLAYER'
    SET_PLAYER = 'SET_PLAYER'
    QUEUE_PLAYER = 'QUEUE_PLAYER'
    GRID_PLAYER = 'GRID_PLAYER'


def player_factory(player_type):
    if player_type == PlayerType.BOT_QUEUE_PLAYER:
        return QueueBot
    if player_type == PlayerType.BOT_GRID_PLAYER:
        return GridBot
    elif player_type == PlayerType.QUEUE_PLAYER:
        return QueuePlayer
    elif player_type == PlayerType.SET_PLAYER:
        return SetPlayer
    elif player_type == PlayerType.GRID_PLAYER:
        return GridPlayer
    return HumanPlayer
