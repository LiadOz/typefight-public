from backend.registers.register import RegisterData
from backend.game.player_factory import PlayerType


def player_reg_factory(player_type):
    if player_type == PlayerType.BOT_QUEUE_PLAYER:
        return None
    elif player_type == PlayerType.QUEUE_PLAYER:
        return PlayerQueueReg
    elif player_type == PlayerType.SET_PLAYER:
        return PlayerReg
    elif player_type == PlayerType.GRID_PLAYER:
        return PlayerReg
    return ObjectRegistration


class ObjectRegistration:
    """
    Registers a certain classes methods
    """

    def __init__(self, obj=None, register=None):
        self.obj = obj
        self.register = register

    def set_register(self, register):
        self.register = register

    def set_obj(self, obj):
        self.obj = obj

    def replace_notify(self, func, data):
        func_name = func.__name__
        new_func = self.register.register_notify(func, data)
        new_func.__name__ = func_name
        setattr(self.obj, func_name, new_func)

    def replace_out(self, func, data):
        func_name = func.__name__
        new_func = self.register.register_out(func, data)
        new_func.__name__ = func_name
        setattr(self.obj, func_name, new_func)

    def register_all(self):
        # this order is important
        self.register_notify()
        self.register_out()
        self.register_in()

    def register_in(self):
        pass

    def register_out(self):
        pass

    def register_notify(self):
        pass


class PlayerReg(ObjectRegistration):
    def register_in(self):
        self.register.register_in(
            RegisterData('publish', self.obj.publish_word))
        self.register.register_in(
            RegisterData('type', lambda x: self.obj.type_key(x['key'])))
        self.register.register_in(
            RegisterData('remove', self.obj.remove_previous, ''))
        self.register.register_in(
            RegisterData('get_data', self.obj.formatted_data, ''))

    def register_out(self):
        self.replace_out(
            self.obj.formatted_data, RegisterData(event='get_data'))

    def register_notify(self):
        out_data = RegisterData('change', self.obj.get_changes)
        fet = self.obj.my_fetcher
        fet.add_change = self.register.register_notify(fet.add_change,
                                                       out_data)
        fet = self.obj.other_fetcher
        fet.add_change = self.register.register_notify(fet.add_change,
                                                       out_data)
        # self.replace_notify(self.obj.remove_previous, out_data)
        # self.replace_notify(self.obj.add_word, out_data)
        # self.replace_notify(self.obj.remove_word, out_data)


class PlayerQueueReg(PlayerReg):
    def register_in(self):
        super().register_in()
        import pdb
        pdb.set_trace()

        self.register.register_in(RegisterData('toggle', self.obj.toggle_mode))


class MatchCreatorReg(ObjectRegistration):
    def register_in(self):
        self.register.register_in(
            RegisterData(event='login', func=self.obj.login_user))
        self.register.register_in(
            RegisterData(event='logged_in', func=self.obj.logged_in))

    def register_out(self):
        self.replace_out(self.obj.login_user, RegisterData(event='login'))


class ExecutorPlayerReg(ObjectRegistration):
    def __init__(self, obj, register, notify_func):
        super().__init__(obj, register)
        self.notify_func = notify_func

    def register_notify(self):
        out_data = RegisterData('out', self.notify_func)
        self.replace_notify(self.obj.type_key, out_data)
        self.replace_notify(self.obj.remove_key, out_data)
        self.replace_notify(self.obj.publish_word, out_data)


class MatchPlayerReg(ObjectRegistration):
    def register_notify(self):
        out = RegisterData('start', self.obj.player.formatted_data)
        self.replace_notify(self.obj.start_playing, out)

        def get_message():
            return {'PLAYER': {'CURRENT': self.obj.get_message()}}

        self.replace_notify(self.obj.change_message,
                            RegisterData('start', get_message))
