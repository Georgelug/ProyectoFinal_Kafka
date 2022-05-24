# server donde van a estar los brokers
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, TextAreaField, StringField,IntegerField,SelectField

from ProducerConsumer import Broker

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'awa de uwu'

brokers = [ Broker(active_status=False, broker_id=1), Broker(active_status=False, broker_id=2)]

class ProducerForm(FlaskForm):
    topic = StringField(name = "Topic")
    message = StringField(name ="Mensaje")
    submitButton = SubmitField("Enviar mensaje")
class ConsumerForm(FlaskForm):
    choicesBrokers = []
    choicesTopics = []
    choicesMensajes = []
    for i in brokers:
        if not i.active_status:
            choicesBrokers.append((i.broker_id,f'broker {i.broker_id}'))
    selectBroker = (SelectField('Seleccionar broker', choices= choicesBrokers) if len(choicesBrokers) > 0 else None) # mejorar esta parte para mostrar un mensaje de error ningun broker esta ocupado en vez de la lista vacia
    selectTopic = SelectField('Seleccionar Topico', choices= choicesTopics)
    selectMessage = SelectField('Seleccionar Mensaje', choices= choicesMensajes)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/Producer1')
def producer1():
    message = ProducerForm()
    print( message.message)
    context ={
        'messageForm': message
    }
    return render_template('producer.html', **context)
@app.route('/Producer2')
def producer2():
    message = ProducerForm()
    print( message.message)
    context ={
        'messageForm': message
    }
    return render_template('producer.html', **context)

@app.route('/Consumer1')
def consumer1():
    message = ConsumerForm()
    print( message.selectMessage)
    context ={
        'messageForm': message
    }
    return render_template('consumer.html', **context)
@app.route('/Consumer2')
def consumer2():
    message = ConsumerForm()
    print( message.selectMessage)
    context ={
        'messageForm': message
    }
    return render_template('consumer.html', **context)


if __name__ == '__main__':
    app.run()
    