from flask import Flask, render_template
from flask import session
from flask import request
from flask import redirect
from flask import send_file
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

socketio = SocketIO(app)
import time
import datetime

start = 0
user = ''
Format = ['','','']

@socketio.on('message')
def handleMessage(msg):
    global start
    if start == 0:
        start = 1
        return
    print("Received name: " + msg['name'])
    print("Received message: " + msg['number2'])
    name = msg['name']
    message = msg['number2']
    times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msglist = Format
    msglist[0] = name
    msglist[1] = times
    msglist[2] = message
    WriteToFile('CHAT', msglist)
    msgs = (f'{msglist[0]} at {msglist[1]} said: {msglist[2]}')
    send(msgs, broadcast=True)

def ReadFile(file):
    s = ""
    with open(f'{file}.txt', 'r') as rara:
        rara1 =  rara.read().splitlines()
        rara1 = rara1[::-1]
        for i in rara1:
            rara2 = i.split('$NEXT$')
            s += (f'{rara2[0]} at {rara2[1]} said: {rara2[2]}\n')
    return s
        

def WriteToFile(file,message):
    with open(f'{file}.txt', 'a') as temp:
        temp.write(message[0])
        temp.write('$NEXT$')
        temp.write(message[1])
        temp.write('$NEXT$')
        temp.write(message[2])
        temp.write('\n')
    return "Hello"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/added', methods=["GET", "POST"])
def added():
    if request.method == "POST":
        name = request.form['number1']
        user = name #makes the input the username
        history = ReadFile('CHAT')
        history = history.split('\n')
        history = '<br>'.join(history)
        if user == "":
            return render_template("index.html")
    return render_template("added.html", name=name, history=history)
    
@app.route('/chat', methods=["POST"])
def chat():
    history = ReadFile('CHAT')
    history = history.split('\n')
    history = '<br>'.join(history)
    return render_template("added.html", history=history)



if __name__ == "__main__":
    socketio.run(app, host = "0.0.0.0")