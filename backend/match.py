from backend.game.player_factory import PlayerType
from backend.game.executor import executor_factory, ExecutorType, PlayerStatus
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
        self.get_match().add_player(player_id)
        self.pending_players.remove(player_id)

    def get_match(self):
        status = self.current_match.get_status()
        if status == MatchStatus.STARTED:
            self.current_match = match_factory(MatchType.SOLO_DUEL)(
                self.object_factory.create_user)
        return self.current_match


class MatchType(Enum):
    SOLO = 1
    SOLO_DUEL = 2
    DUEL = 2
    ROYALE = 100


class MatchStatus(Enum):
    OPEN = 1
    STARTED = 2


def match_factory(match_type):
    if match_type == MatchType.SOLO_DUEL:
        return SoloDuelMatch
    elif match_type == MatchType.DUEL:
        return DuelMatch


class MatchStarter:
    START_TIME = 2

    def __init__(self, human_players, bot_players, executor):
        self.human_players = human_players
        self.bot_players = bot_players
        self.executor = executor

    # initialize all the players
    def _init_match(self):
        for player in self.human_players:
            player.init_player(self.executor)
        for player in self.bot_players:
            player.init_player(self.executor)
        self.executor.init_game()

    # start the game
    def _start_match(self):
        from time import sleep
        for sec in range(MatchStarter.START_TIME, 0, -1):
            for player in self.human_players:
                player.change_message(f'Starting in {sec}')
            sleep(1)

        self.executor.start_game()
        for player in self.human_players:
            player.start_playing()
        for player in self.bot_players:
            player.start_playing()

    def start(self):
        self._init_match()
        self._start_match()


class Match:
    def __init__(self, capacity, player_creator):
        self.capacity = capacity
        self.player_creator = player_creator
        self.active_players = {}
        self.active_bots = {}
        self.status = MatchStatus.OPEN

    def get_status(self):
        return self.status

    def add_player(self, player_id):
        if len(self.active_players) >= self.capacity:
            raise Exception('Cant add more players')
        self.active_players[player_id] = self.player_creator(
            PlayerType.GRID_PLAYER, player_id)
        if len(self.active_players) + len(self.active_bots) == self.capacity:
            self.start_match()

    def add_bot(self):
        # the given player id is zero, some better design is needed
        self.active_bots[0] = \
            self.player_creator(PlayerType.BOT_GRID_PLAYER, 0)

    def remove_player(self, match_player):
        self.active_players.pop(match_player.player_id)

    def start_match(self):
        self.status = MatchStatus.STARTED
        ms = MatchStarter(self.active_players.values(),
                          self.active_bots.values(), self.executor)
        ms.start()


def end_callback(orig, added):
    def _end_callback(*args, **kwargs):
        orig(*args, **kwargs)
        added()

    return _end_callback


class TwoPlayerMatch(Match):
    def __init__(self, match_type, player_creator):
        super().__init__(match_type, player_creator)
        self.executor = executor_factory(ExecutorType.DUEL)

        self.executor.end_game = end_callback(
            self.executor.end_game, self._end_match)


    def _end_match(self):
        ps = self.executor.get_players_status()
        for p_id, bot in self.active_bots.items():
            bot.stop_playing()

        for p_id, player in self.active_players.items():
            player.stop_playing()  # TODO no implementation
            status = ps[p_id].value
            if status == PlayerStatus.WINNER:
                player.change_message('Game ended you won!')
            elif status == PlayerStatus.LOSER:
                player.change_message('Game ended you lost!')
            else:
                player.change_message('Game ended with an error!')


class DuelMatch(TwoPlayerMatch):
    def __init__(self, player_creator):
        super().__init__(MatchType.DUEL.value, player_creator)


class SoloDuelMatch(TwoPlayerMatch):
    def __init__(self, player_creator):
        super().__init__(MatchType.SOLO_DUEL.value, player_creator)
        self.add_bot()


class MatchPlayer:
    def __init__(self, player, player_id):
        self.player = player
        self.player_id = player_id

    def init_player(self, executor):
        self.player.attach_executor(executor)

    def start_playing(self):
        pass

    def stop_playing(self):
        pass


class HumanMatchPlayer(MatchPlayer):
    def __init__(self, player, player_id, player_reg):
        super().__init__(player, player_id)
        self.player_reg = player_reg
        self.change_message('Waiting for match to start...')

    def change_message(self, message):
        self.player_message = message

    def get_message(self):
        return self.player_message

    def start_playing(self):
        self.player.register_fetchers()
        self.player_reg.register_all()


class BotMatchPlayer(MatchPlayer):
    def __init__(self, player):
        self.player = player
        self.player_id = player.u_id

    def start_playing(self):
        self.player.start_playing()

    def stop_playing(self):
        self.player.stop_playing()
