import json
import requests


# the model currently handles one game
class Model:
    def __init__(self, endpoint='http://127.0.0.1:5000'):
        self.endpoint = endpoint
        self.user = json.loads(
            requests.get(f"{endpoint}/register").text)['id']
        print(self.user)

    def get_data(self):
        return json.loads(requests.get(self.endpoint + '/get_data',
                                       data={'id': self.user}).text)

    def send_letter(self, letter):
        payload = {'id': self.user, 'key': letter}
        requests.post(self.endpoint + '/type', data=payload)

    def remove_letter(self):
        requests.post(self.endpoint + '/remove', data={'id': self.user})

    def publish_current_word(self):
        requests.post(self.endpoint + '/publish', data={'id': self.user})

    def switch_typing_mode(self, event=None):
        requests.post(self.endpoint + '/toggle', data={'id': self.user})
