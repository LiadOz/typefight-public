from backend.players import QueuePlayer, executor_factory
from backend.generate import WordGenerator
from backend.register import PlayerRegistrationQueue
from backend.bots import BotPlayer
from common.utility import WordType
from enum import Enum


class MatchCreator:
    def __init__(self, register, id_store):
        self.register = register
        self.id_store = id_store
        self.current_match = RegularMatch(MatchType.DUEL)

    def login_user(self):
        player_id = self.id_store.get_new_id()
        register = self.register.child_register(f"/data{player_id}")
        player = MatchPlayer(
            QueuePlayer,
            player_id,
            PlayerRegistrationQueue(register=register))
        self.current_match.add_player(player)
        player2 = BotMatchPlayer(BotPlayer, self.id_store.get_new_id())
        self.current_match.add_player(player2)
        return player_id


class MatchType(Enum):
    SINGLE_PLAYER = 1
    DUEL = 2
    ROYALE = 3


class Match:
    pass


class MatchPlayer:
    def __init__(self, player_class, player_id, registration):
        self.player_class = player_class
        self.player_id = player_id
        self.registration = registration

    def create_player(self, executor):
        self.player = self.player_class(executor, self.player_id)
        self.registration.set_obj(self.player)

    # the word generator should move out of here
    def start_playing(self, word_gen):
        for _ in range(10):
            self.player.add_word(WordType.ATTACK, word_gen.get_word())
            self.player.add_word(WordType.DEFEND, word_gen.get_word())
        self.registration.register_all()


class BotMatchPlayer(MatchPlayer):
    def __init__(self, player_class, player_id):
        self.player_class = player_class
        self.player_id = player_id

    def create_player(self, mediator):
        self.player = self.player_class(mediator, self.player_id)

    def start_playing(self, word_gen):
        for _ in range(10):
            self.player.add_word(WordType.ATTACK, word_gen.get_word())
            self.player.add_word(WordType.DEFEND, word_gen.get_word())
        self.player.start_playing()


class RegularMatch(Match):
    def __init__(self, match_type):
        self.executor = executor_factory(match_type.value)
        self.capacity = match_type.value
        self.word_generator = WordGenerator()
        self.active_players = {}

    def add_player(self, match_player):
        if len(self.active_players) >= self.capacity:
            raise Exception('Cant add more players')
        match_player.create_player(self.executor)
        self.active_players[match_player.player_id] = match_player
        if len(self.active_players) == self.capacity:
            self.start_match()

    def remove_player(self, match_player):
        self.active_players.pop(match_player.player_id)

    def start_match(self):
        for player in self.active_players.values():
            player.start_playing(self.word_generator)
