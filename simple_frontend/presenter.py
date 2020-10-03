from functools import wraps
from .model import Model
from .view import View


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
        # self.render_game()
        self.view.run()

    def render_game(self, data=None):
        if not data:
            data = self.model.get_data()
        self.view.render_game(data)

    @_write_action
    def send_letter(self, event):
        self.model.send_letter(event.char)

    # the events could be removed using lambda function in view module
    @_write_action
    def remove_letter(self, event=None):
        self.model.remove_letter()

    @_write_action
    def publish_current_word(self, event=None):
        self.model.publish_current_word()

    @_write_action
    def switch_user(self, event=None):
        # self.model.switch_user()
        pass

    def switch_typing_mode(self, event=None):
        self.model.switch_typing_mode()


if __name__ == '__main__':
    app = Presenter()
    app.run()
