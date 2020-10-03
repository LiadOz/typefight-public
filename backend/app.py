from backend.game import Game
from flask import Flask, request
from json import dumps

game = Game()
game.demo_setup()
user_1, user_2 = None, None
active_users = 0
app = Flask(__name__)


@app.route('/')
def start():
    return 'you are connected'


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


@app.route('/get_data', methods=['GET', 'POST'])
def data():
    user = curr_user(request.form['id'])
    return dumps(user.get_data())


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
