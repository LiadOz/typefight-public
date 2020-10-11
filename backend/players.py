from common.utility import Word, WordType
from backend.player_words import create_player_words, PlayerWordsType
from enum import Enum


def mediator_factory(count):
    if count == 1:
        return None
    if count == 2:
        return DuelMediator()
    else:
        return RoyaleMediator()


class PlayerMediator:
    def register_player(self, player):
        pass

    def send_action(self, caller, action):
        pass


class DuelMediator(PlayerMediator):
    def __init__(self):
        self.registered = 0

    def register_player(self, player):
        if self.registered == 0:
            self.player_1 = player
            self.u_id_1 = player.u_id
            self.registered += 1
        elif self.registered == 1:
            self.player_2 = player
            self.u_id_2 = player.u_id
            self.registered += 1
        else:
            raise Exception('Only two users allowed in duel')

    def send_action(self, caller, action):
        return self.get_opponent(caller).recieve_action(action)

    def get_opponent(self, caller):
        # this should be changed to depend on player_id so that you
        # could change the functions of a player
        if caller.u_id == self.u_id_1:
            return self.player_2
        if caller.u_id == self.u_id_2:
            return self.player_1
        raise Exception('Unknown caller')


class RoyaleMediator(PlayerMediator):
    pass


class Action:
    def __init__(self, action, data):
        self.action = action
        self.data = data


class ActionType(Enum):
    ATTACK = 1
    DEFEND = 2
    TYPE = 3
    GET_DEFEND = 4
    GET_ATTACK = 5


class ActionExecuter:
    def __init__(self, player):
        self.player = player

    def execute(self, action):
        pass


class SimpleExecuter(ActionExecuter):
    def execute(self, action):
        if action.action is ActionType.ATTACK:
            self.player.add_word(WordType.DEFEND, action.data)
            print('remove word', self.player.add_word)
        elif action.action is ActionType.GET_DEFEND:
            return self.player.get_data()[WordType.DEFEND]


class IPlayer:
    def __init__(self, mediator, u_id):
        self.u_id = u_id
        self.mediator = mediator
        self.mediator.register_player(self)

    def recieve_action(self, action):
        pass


class Player(IPlayer):
    def __init__(self, mediator, player_words_type, executer, u_id):
        super().__init__(mediator, u_id)
        self.current_word = Word()
        self.words = create_player_words(player_words_type)
        self.executer = executer(self)

    def type_key(self, key):
        self.current_word.add_letter(key)

    def remove_previous(self):
        self.current_word.remove_letter()

    def add_word(self, w_type, word):
        self.words.add_word(w_type, word)

    def remove_word(self, w_type, word):
        self.words.remove_word(w_type, word)

    def publish_word(self):
        pass

    def get_data(self):
        payload = self.words.format()
        payload['CURRENT'] = self.current_word.get_text()
        return payload

    def recieve_action(self, action):
        return self.executer.execute(action)


class HumanPlayer(Player):
    def __init__(self, *args):
        super().__init__(*args)

    def get_game_data(self):
        payload = self.get_data()
        rival = self.mediator.send_action(self,
                                          Action(ActionType.GET_DEFEND, None))
        payload[WordType.RIVAL] = rival
        return payload

    def formatted_data(self):
        original = self.get_game_data()
        ret = {}
        for w_type in WordType:
            ret[w_type.value] = original[w_type]
        for k in original:
            if k in WordType:
                continue
            ret[k] = original[k]
        return ret


class BotPlayer(Player):
    pass


class PlayerQueueAndMode(HumanPlayer):
    def __init__(self, mediator, u_id):
        super().__init__(mediator, PlayerWordsType.QUEUE, SimpleExecuter, u_id)
        self.mode = WordType.DEFEND

    def publish_word(self):
        q = self.get_data()[self.mode]
        if q and q[0] == self.current_word.get_text():
            if self.mode == WordType.ATTACK:
                self.mediator.send_action(self, Action(ActionType.ATTACK,
                                                       q[0]))
            self.current_word.reset_word()
            self.remove_word(self.mode, 0)

    def toggle_mode(self):
        if self.mode == WordType.ATTACK:
            self.mode = WordType.DEFEND
        else:
            self.mode = WordType.ATTACK


class PlayerSet(HumanPlayer):
    def __init__(self, mediator):
        super().__init__(mediator, PlayerWordsType.SET, SimpleExecuter)
