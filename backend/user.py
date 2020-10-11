# this should someday be hooked to a database
class IdStore:
    def __init__(self):
        self.count = 1

    def get_new_id(self):
        ret = self.count
        self.count += 1
        return ret
