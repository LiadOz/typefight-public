from backend.players import QueuePlayer, executor_factory
from backend.generate import WordGenerator
from backend.register import PlayerRegistrationQueue
from backend.bots import BotPlayer
from common.utility import WordType
from enum import Enum


# this should become human player
class MatchPlayer:
    def __init__(self, player, registration):
        self.player = player
        self.player_id = player.u_id
        self.registration = registration

    # the word generator should move out of here
    def start_playing(self, word_gen):
        for _ in range(10):
            self.player.add_word(WordType.ATTACK, word_gen.get_word())
            self.player.add_word(WordType.DEFEND, word_gen.get_word())
        self.registration.register_all()


class BotMatchPlayer(MatchPlayer):
    def __init__(self, player):
        self.player = player
        self.player_id = player.u_id

    def start_playing(self, word_gen):
        for _ in range(10):
            self.player.add_word(WordType.ATTACK, word_gen.get_word())
            self.player.add_word(WordType.DEFEND, word_gen.get_word())
        self.player.start_playing()


class PlayerCreator:
    def __init__(self, register, id_store):
        self.register = register
        self.id_store = id_store

    def create_user(self, player_type, executor):
        player_id = self.id_store.get_new_id()
        if player_type == 'HUMAN':
            player = QueuePlayer(executor, player_id)
            register = self.register.child_register(f"/data{player_id}")
            registration = PlayerRegistrationQueue(player, register)
            player = MatchPlayer(player, registration)
        else:
            player = BotMatchPlayer(BotPlayer(executor, player_id))
        return player


class MatchCreator:
    def __init__(self, player_creator):
        self.player_creator = player_creator
        self.current_match = RegularMatch(MatchType.DUEL)

    def login_user(self):
        player = self.player_creator.create_user(
            'HUMAN', self.current_match.executor)
        self.current_match.add_player(player)
        player2 = self.player_creator.create_user(
            'COM', self.current_match.executor)
        self.current_match.add_player(player2)
        return player.player_id


class MatchType(Enum):
    SINGLE_PLAYER = 1
    DUEL = 2
    ROYALE = 3


class Match:
    pass




class RegularMatch(Match):
    def __init__(self, match_type):
        self.executor = executor_factory(match_type.value)
        self.capacity = match_type.value
        self.word_generator = WordGenerator()
        self.active_players = {}

    def add_player(self, match_player):
        if len(self.active_players) >= self.capacity:
            raise Exception('Cant add more players')
        self.active_players[match_player.player_id] = match_player
        if len(self.active_players) == self.capacity:
            self.start_match()

    def remove_player(self, match_player):
        self.active_players.pop(match_player.player_id)

    def start_match(self):
        for player in self.active_players.values():
            player.start_playing(self.word_generator)
