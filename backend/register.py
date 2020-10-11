from functools import wraps
from json import dumps
from flask_socketio import emit
from enum import Enum
from pdb import set_trace as bp


class Register:
    """
    Handles the how things are registered
    """

    def __init__(self, obj, endpoint):
        self.obj = obj
        self.endpoint = endpoint

    def child_register(self, sub_endpoint):
        return type(self)(self.obj, self.endpoint + sub_endpoint)

    def register_in(self, func, data):
        pass

    def create_callback(func, callback, data, ret_value=True):
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            if ret_value:
                data.data = ret
            callback(data)

        return wrapper

    def register_out(self, func, data):
        print(f"registering event '{data.event}' from '{self.endpoint}'")
        return Register.create_callback(
            func, self._out_function, data)

    def register_notify(self, func, data):
        print(f"registering event '{data.event}' from '{self.endpoint}'")
        return Register.create_callback(
            func, self._notify_function, data, False)

    def _notify_function(self):
        pass

    def _out_function(self):
        pass


class ResgisterType(Enum):
    pass


class RegisterData:
    def __init__(self, event=None, func=None, data=None):
        self.event = event
        self.data = data
        self.func = func


class SocketRegister(Register):
    def __init__(self, obj, endpoint):
        self.obj = obj
        self.endpoint = endpoint

    def register_in(self, data):
        self.obj.on_event(data.event, data.func)
        print(f"registering event '{data.event}' to '{self.endpoint}'")

    def _notify_function(self, data):
        if data.func:
            self.obj.emit(data.event, dumps(data.func()))
        elif data.data:
            self.obj.emit(data.event, data.data)

    def _out_function(self, data):
        emit(data.event, data.data)


class RequestRegister(Register):
    pass


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

    def register_all(self):
        self.register_out()
        self.register_notify()
        self.register_in()

    def register_in(self):
        pass

    def register_out(self):
        pass

    def register_notify(self):
        pass


class NewObjectRegistration:
    """
    Registers a certain classes methods
    """

    def __init__(self, register):
        self.register = register

    def register_all(self):
        self.register_out()
        self.register_notify()

        self.register_in()

    def register_in(self):
        pass

    def register_out(self):
        pass

    def register_notify(self):
        pass


class PlayerRegistration(ObjectRegistration):
    def register_all(self):
        reg = self.register
        out_data = RegisterData('out', self.obj.formatted_data)
        self.obj.type_key = reg.register_notify(
            self.obj.type_key, out_data)
        self.obj.remove_previous = reg.register_notify(
            self.obj.remove_previous, out_data)
        self.obj.add_word = reg.register_notify(
            self.obj.add_word, out_data)
        self.obj.remove_word = reg.register_notify(
            self.obj.remove_word, out_data)

        reg.register_in(
            RegisterData('type', lambda x: self.obj.type_key(x['key'])))
        reg.register_in(RegisterData('remove', self.obj.remove_previous, ''))


class PlayerRegistrationQueue(PlayerRegistration):
    def register_all(self):
        super().register_all()

        self.register.register_in(
            RegisterData('publish', self.obj.publish_word))
        self.register.register_in(RegisterData('toggle', self.obj.toggle_mode))
