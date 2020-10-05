from backend.game import Game
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from json import dumps

game = Game()
game.demo_setup()
user_1, user_2 = None, None
active_users = 0
app = Flask(__name__)
app.config['SECRET_KEY'] = 's'
socket = SocketIO(app, logger=True)


def run():
    socket.run(app)


@app.route('/')
def start():
    return render_template('test.html')


@app.route('/register')
def register():
    global active_users, user_1, user_2
    if active_users == 0:
        user_1 = game.register_user()
    else:
        user_2 = game.register_user()
    active_users += 1
    return dumps({'id': active_users})


def curr_user(num):
    if int(num) == 1:
        return user_1
    return user_2


# This is not used to constantly send data!
@socket.on('get_data', namespace='/game')
def data(json):
    data = curr_user(json['id']).get_data()
    emit('data_resp', dumps(data), namespace='/data' + json['id'])


def send_data(u_id, data):
    print(u_id)
    socket.emit('data', dumps(data), namespace='/data' + u_id)


@app.route('/type', methods=['GET', 'POST'])
def type():
    user = curr_user(request.form['id'])
    user.type_key(request.form['key'])
    return ''


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    user = curr_user(request.form['id'])
    user.remove_previous()
    return ''


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    user = curr_user(request.form['id'])
    user.publish_word()
    return ''


@app.route('/toggle', methods=['GET', 'POST'])
def toggle():
    user = curr_user(request.form['id'])
    user.toggle_mode()
    return ''


game.set_broadcast(send_data)
