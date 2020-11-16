from backend.game.player_factory import PlayerType
from backend.game.executor import executor_factory, ExecutorType, PlayerStatus
from backend.user import IdStore
from enum import Enum


class MatchType(Enum):
    SOLO = 'SOLO'
    SOLO_DUEL = 'SOLO_DUEL'
    DUEL = 'DUEL'
    ROYALE = 'ROYALE'

    @classmethod
    def parse_match(cls, match_type):
        for m_type in MatchType:
            if m_type.value == match_type:
                return m_type
        raise RuntimeError(f'Unknown match type {match_type}')


class MatchCreator:
    def __init__(self, object_factory):
        self.object_factory = object_factory
        self.open_matches = {}
        self.id_store = IdStore()
        self.pending_players = {}

    # this along the idstore should move to a class which handles login
    def login_user(self, data):
        player_id = self.id_store.get_new_id()
        match_type = data['match_type']
        self.pending_players[player_id] = MatchType.parse_match(match_type)
        return player_id

    def logged_in(self, data):
        player_id = data['id']
        match_type = self.pending_players.pop(player_id)
        self.get_match(match_type).add_player(player_id)

    def get_match(self, match_type):
        match = self.open_matches.get(match_type)
        if not match or match.get_status() == MatchStatus.STARTED:
            match = match_factory(match_type)(self.object_factory.create_user)
            self.open_matches[match_type] = match
        return match


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
            status = ps[p_id]
            if status is PlayerStatus.WINNER:
                player.change_message('You won!')
            elif status is PlayerStatus.LOSER:
                player.change_message('You lost!')
            else:
                player.change_message('Game ended with an error!')


class DuelMatch(TwoPlayerMatch):
    def __init__(self, player_creator):
        super().__init__(2, player_creator)


class SoloDuelMatch(TwoPlayerMatch):
    def __init__(self, player_creator):
        super().__init__(2, player_creator)
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
