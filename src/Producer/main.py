# server donde van a estar los brokers
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField, StringField

from ProducerConsumer import Broker

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'awa de uwu'
 
#brokers = [ Broker(active_status=True, broker_id=1), Broker(active_status=True, broker_id=2)]

class ProducerForm(FlaskForm):
    topic = StringField(name = "Topic")
    message = TextAreaField(name ="Mensaje")
    submitButton = SubmitField("Enviar mensaje")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Producer1', methods=['GET', 'POST'])
def producer1():
    message = ProducerForm()
    context ={
        'messageForm': message
    }
    return render_template('producer.html', **context)

if __name__ == '__main__':
    app.run()
    