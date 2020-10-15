from backend.registers.register import register_factory
from backend.game.player_factory import player_factory
from backend.registers.registors import player_reg_factory, MatchPlayerReg
from backend.match import MatchPlayer, BotMatchPlayer


class MainRegister:
    def __init__(self, register_type, obj, endpoint):
        self.register = register_factory(register_type, obj, endpoint)
        self.player_factory = PlayerFactory(self.register)

    def create_user(self, player_type, player_id):
        return self.player_factory.create_user(player_type,
                                               player_id)


class PlayerFactory:
    def __init__(self, register):
        self.register = register

    def create_user(self, player_type, player_id):
        player = player_factory(player_type)(player_id)
        register = self.register.child_register(f"/data{player_id}")
        player_reg = player_reg_factory(player_type)
        if player_reg:
            player_reg = player_reg(player, register)
            player = MatchPlayer(player, player_id, player_reg)
            # this should all be done in one step
            # maybe the matchplayerreg handles the registration of player
            MatchPlayerReg(player, register).register_all()
        else:
            player = BotMatchPlayer(player)
        return player
