# server donde van a estar los brokers
from flask import Flask, render_template, request,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired

import zmq
import sys
from time import sleep

#from tools.ProducerConsumer import Broker

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'awa de uwu'
 
context = zmq.Context()
#  Socket to talk to server
print("Connecting to the brokers …")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

class ProducerForm(FlaskForm):
    topic = StringField("Topic", validators=[DataRequired()])
    message = TextAreaField("Mensaje",validators=[DataRequired()])
    submitButton = SubmitField("Enviar mensaje")


@app.route('/')
def home():
    return render_template('producer.html')

@app.route('/Producer', methods=['GET', 'POST'])
def producer():
    messageForm = ProducerForm()
    context ={
        'messageForm': messageForm
    }
    
    if messageForm.validate_on_submit:
        socket.send_pyobj({'mode':'publish','message':(messageForm.topic.data,messageForm.message.data)}) # se manda un diccionario donde se tiene el modo publish y el topic junto con un mensaje
        messageBroker = socket.recv_string() # se recibe la notificacion de recibido
        print(messageBroker)
        sleep(1)
        messageForm.topic.data = ""
        messageForm.message.data = ""

    return render_template('producer.html', **context)

if __name__ == '__main__':
    app.run()
    