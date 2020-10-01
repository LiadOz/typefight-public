from functools import wraps
from .model import Model
from .view import View
from common.utility import WordType


class Presenter:
    def __init__(self):
        self.model = Model()
        self.view = View(self)

    def _write_action(func):
        @wraps(func)
        def wrapper(inst, *args, **kwargs):
            ret = func(inst, *args, **kwargs)
            inst.render_game(ret)
        return wrapper

    def run(self):
        self.render_game()
        self.view.run()

    def render_game(self, data=None):
        if not data:
            data = self.model.active_user.get_data()
        self.view.render_game(data)

    @_write_action
    def send_letter(self, event):
        self.model.active_user.type_key(event.char)

    # the events could be removed using lambda function in view module
    @_write_action
    def remove_letter(self, event=None):
        self.model.active_user.remove_previous()

    @_write_action
    def publish_current_word(self, event=None):
        self.model.active_user.publish_word()

    @_write_action
    def switch_user(self, event=None):
        self.model.switch_user()

    def switch_typing_mode(self, event=None):
        self.model.active_user.toggle_mode()


if __name__ == '__main__':
    app = Presenter()
    app.run()
