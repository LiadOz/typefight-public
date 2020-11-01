from flask import Flask, render_template
from flask_socketio import SocketIO
from backend.registers.registors import MatchCreatorReg
from backend.registers.register import RegisterType, SocketRegister
from backend.register import MainRegister
from backend.match import MatchCreator
import logging

app = Flask(__name__, template_folder='../frontend',
            static_folder='../frontend/static')
logging.getLogger('werkzeug').disabled = True
# HACK should register in another way

@app.route('/')
def root():
    import os
    return render_template('start.html')

app.config.from_object('backend.config.Config')
sio = SocketIO(app, logger=True)
mr = MainRegister(RegisterType.SOCKET, sio, '')

tempregister = SocketRegister(sio, '')
match = MatchCreator(mr)
MatchCreatorReg(match, tempregister).register_all()


def run():
    sio.run(app)
