from flask import Flask
from flask_socketio import SocketIO
from backend.registers.registors import MatchCreatorReg
from backend.registers.register import RegisterType, SocketRegister
from backend.register import MainRegister
from backend.match import MatchCreator
import logging

app = Flask(__name__)
logging.getLogger('werkzeug').disabled = True
app.config.from_object('backend.config.Config')
sio = SocketIO(app, logger=False)
mr = MainRegister(RegisterType.SOCKET, sio, '')

tempregister = SocketRegister(sio, '')
match = MatchCreator(mr)
MatchCreatorReg(match, tempregister).register_all()


def run():
    sio.run(app)
