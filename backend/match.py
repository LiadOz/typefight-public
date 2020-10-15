from backend.game.player_factory import PlayerType
from backend.game.executor import executor_factory, ExecutorType
from backend.user import IdStore
from enum import Enum


class MatchCreator:
    def __init__(self, object_factory):
        self.object_factory = object_factory
        self.current_match = match_factory(MatchType.SOLO_DUEL)(
            object_factory.create_user)
        self.id_store = IdStore()
        self.pending_players = set()

    # this along the idstore should move to a class which handles login
    def login_user(self):
        player_id = self.id_store.get_new_id()
        self.pending_players.add(player_id)
        return player_id

    def logged_in(self, data):
        player_id = data['id']
        self.current_match.add_player(player_id)
        self.pending_players.remove(player_id)


class MatchType(Enum):
    SOLO = 1
    SOLO_DUEL = 2
    DUEL = 2
    ROYALE = 100


def match_factory(match_type):
    if match_type == MatchType.SOLO_DUEL:
        return SoloDuelMatch
    elif match_type == MatchType.DUEL:
        return DuelMatch


class Match:
    def __init__(self, capacity, player_creator):
        self.capacity = capacity
        self.player_creator = player_creator
        self.active_players = {}

    def add_player(self, player_id):
        if len(self.active_players) >= self.capacity:
            raise Exception('Cant add more players')
        self.active_players[player_id] = self.player_creator(
            PlayerType.SET_PLAYER, player_id)
        if len(self.active_players) == self.capacity:
            self.init_match()
            self.start_match()

    def add_bot(self):
        # the given player id is zero, some better design is needed
        self.active_players[0] = self.player_creator(
            PlayerType.BOT_QUEUE_PLAYER, 0)

    def remove_player(self, match_player):
        self.active_players.pop(match_player.player_id)

    # first stage of starting a game
    def init_match(self):
        for player in self.active_players.values():
            player.init_player(self.executor)
        self.executor.init_game()

    # last stage of starting a game
    def start_match(self):
        for player in self.active_players.values():
            player.start_playing()


class DuelMatch(Match):
    def __init__(self, player_creator):
        super().__init__(MatchType.DUEL.value, player_creator)
        self.executor = executor_factory(ExecutorType.DUEL)


class SoloDuelMatch(Match):
    def __init__(self, player_creator):
        super().__init__(MatchType.SOLO_DUEL.value, player_creator)
        self.executor = executor_factory(ExecutorType.DUEL)
        self.add_bot()


# this should become human player
class MatchPlayer:
    def __init__(self, player, player_id, player_reg):
        self.player = player
        self.player_id = player_id
        self.player_reg = player_reg

    # the word generator should move out of here
    def init_player(self, executor):
        self.player.attach_executor(executor)

    def start_playing(self):
        self.player.register_fetchers()
        self.player_reg.register_all()


class BotMatchPlayer(MatchPlayer):
    def __init__(self, player):
        self.player = player
        self.player_id = player.u_id

    def start_playing(self):
        self.player.start_playing()
