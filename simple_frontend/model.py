import json
import requests
from socketio import Client


# the model currently handles one game
class Model:
    def __init__(self, render, endpoint='http://127.0.0.1:5000'):
        self.endpoint = endpoint
        self.user = json.loads(
            requests.get(f"{endpoint}/register").text)['id']
        self.socket = Client(logger=True)
        self.socket.connect(endpoint, namespaces=[f"/data{self.user}"])
        self.socket.on('data', render, namespace=f"/data{self.user}")
        print(self.user)

    # def get_data(self):
    #     return json.loads(requests.get(self.endpoint + '/get_data',
    #                                    data={'id': self.user}).text)

    def send_letter(self, letter):
        payload = {'id': self.user, 'key': letter}
        requests.post(self.endpoint + '/type', data=payload)

    def remove_letter(self):
        requests.post(self.endpoint + '/remove', data={'id': self.user})

    def publish_current_word(self):
        requests.post(self.endpoint + '/publish', data={'id': self.user})

    def switch_typing_mode(self, event=None):
        requests.post(self.endpoint + '/toggle', data={'id': self.user})
