# coding: utf-8

# HerbaChat Client made by HerbeMalveillante
# http://projetcharbon.tk

# importation of necessary modules :
from flask import Flask
from flask import render_template
from flask import request
from flask_socketio import SocketIO
from time import *
import socket

########## Misc Functions ##########


def get_ip_address():  # returns server ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_hour():
    date = ctime(time())
    hour = "[" + date[11:16] + "] "
    return hour

########## SocketIo and Flask configuration ##########


app = Flask(__name__) # Flask server configuration
socketio = SocketIO(app)


# definition of the default app route (index page)
@app.route("/")
def index():
    return render_template("home.html")

########## Reception from the socket ##########


@socketio.on('connectionClient-->Server')
def on_connection(client_username):
    print(get_hour() + client_username + " just connected.")
    socketio.emit('confirmConnectionServer-->Client', client_username)
    print("emitted connection confirmation for " + client_username)


@socketio.on('messageClient-->Server')
def on_message(message):
    message_content = message[0]
    message_author = message[1]
    print(get_hour() + message_author + " : " + message_content)
    socketio.emit('confirmMessageServer-->Client', message)

if __name__ == '__main__':
    print("")
    server_ip_address = get_ip_address()
    print("server's IP address : http://"+str(server_ip_address)+":5000")
    print("")
    socketio.run(app, host=server_ip_address, port=5000)



