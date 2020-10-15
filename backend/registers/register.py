from functools import wraps
from json import dumps
from flask_socketio import emit
from enum import Enum


class RegisterType(Enum):
    SOCKET = 'SOCKET'
    HTTP = 'HTTP'


def register_factory(register_type, obj, endpoint):
    if register_type == RegisterType.SOCKET:
        return SocketRegister(obj, endpoint)
    elif register_type == RegisterType.HTTP:
        return RequestRegister(obj, endpoint)
    return Register(obj, endpoint)


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
            return ret

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
        self.obj.on_event(data.event, data.func, namespace=self.endpoint)
        print(f"registering event '{data.event}' to '{self.endpoint}'")

    def _notify_function(self, data):
        if data.func:
            self.obj.emit(
                data.event, dumps(data.func()), namespace=self.endpoint)
        elif data.data:
            self.obj.emit(data.event, data.data, namespace=self.endpoint)

    def _out_function(self, data):
        emit(data.event, data.data, namespace=self.endpoint)


class RequestRegister(Register):
    pass
