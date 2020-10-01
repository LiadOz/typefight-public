from backend.game import Game


# the model currently handles one game
class Model:
    def __init__(self):
        self.game = Game()
        self.game.demo_setup()
        self.active_user_flag = 0
        self.user_1 = self.game.register_user()
        self.user_2 = self.game.register_user()
        self.active_user = self.user_1
        print(self.active_user.get_data())

    def switch_user(self):
        if self.active_user_flag:
            self.active_user = self.user_2
        else:
            self.active_user = self.user_1
        self.active_user_flag = not self.active_user_flag
