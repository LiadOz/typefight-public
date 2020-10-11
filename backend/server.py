from flask import Flask
from flask_socketio import SocketIO
from backend.register import SocketRegister
from backend.class_registers import MatchCreatorReg
from backend.match import MatchCreator
from backend.user import IdStore
import logging

app = Flask(__name__)
logging.getLogger('werkzeug').disabled = True
app.config.from_object('backend.config.Config')
sio = SocketIO(app, logger=True)

register = SocketRegister(sio, '')
match = MatchCreatorReg(register, IdStore(), register)
match.register_all()


def run():
    sio.run(app)
