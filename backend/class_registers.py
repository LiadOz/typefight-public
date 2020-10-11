from backend.register import NewObjectRegistration, RegisterData
from backend.match import MatchCreator
from backend.players import PlayerQueueAndMode


class MatchCreatorReg(MatchCreator, NewObjectRegistration):
    def __init__(self, match_register, id_store, register):
        MatchCreator.__init__(self, match_register, id_store)
        NewObjectRegistration.__init__(self, register)

    def register_in(self):
        self.register.register_in(
            RegisterData(event='login', func=self.login_user))

    def register_out(self):
        self.login_user = self.register.register_out(
            self.login_user, RegisterData(event='login'))
