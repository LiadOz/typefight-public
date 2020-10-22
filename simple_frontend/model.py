from socketio import Client


# the model currently handles one game
class Model:
    def __init__(self, render, render_change,
                 endpoint='http://127.0.0.1:5000'):
        self.endpoint = endpoint
        self.render = render
        self.render_change = render_change
        # self.user = json.loads(
        #     requests.get(f"{endpoint}/register").text)['id']
        self.socket = Client(logger=False)
        self.socket.on('login', self.register_self)
        self.socket.connect(endpoint)
        self.socket.emit('login')

    # def get_data(self):
    #     return json.loads(requests.get(self.endpoint + '/get_data',
    #                                    data={'id': self.user}).text)

    def register_self(self, player):
        # to do this correctly you would need to use rooms
        self.namespace = f"/data{player}"
        self.socket = Client(logger=True)  # this is bad
        self.socket.connect(self.endpoint, namespaces=[self.namespace])
        self.socket.emit('logged_in', {'id': player})
        self.socket.on('start', self.render, namespace=self.namespace)
        self.socket.on('change', self.render_change, namespace=self.namespace)

    def send_letter(self, letter):
        self.socket.emit('type', {'key': letter}, namespace=self.namespace)

    def remove_letter(self):
        self.socket.emit('remove', namespace=self.namespace)

    def publish_current_word(self):
        self.socket.emit('publish', namespace=self.namespace)

    def switch_typing_mode(self, event=None):
        self.socket.emit('toggle', namespace=self.namespace)
