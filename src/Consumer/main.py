#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import sys
import os
from time import sleep
from random import seed
from random import randint
from flask import Flask, render_template, request
sys.path.insert(0,'/home/alejandro/Sistemas_distribuidos/ProyectoFinal_Kafka/src/tools')
from ProducerConsumer import *

seed(1)
context = zmq.Context()
consumer = Consumer()
#  Socket to talk to server
print("Connecting to Consumer client...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

def selectBroker(message):
    if message[1] and message[2]: # si ambos brokers estan ocupados regresa None
        #bandera = False
        return None
    if message[2]: # si el broker 2 esta ocupado regresa 1
        #bandera = True
        return 1
    if message[1]: # si el broker 1 esta ocupado regresa 2
        #bandera = True
        return 2
    return randint(1,2)

# se envia una peticion de modo consume
sleep(1)
socket.send_pyobj({'mode':'consume'})

consumer.setConsumingStatus(True) # se cambia el estado del conusmer a activo, es decir, esta consumiendo
sleep(1)
message = socket.recv_pyobj() # se recibe un diccionario {1:<estado>,2:<estado>}
consumer.setBrokerId(selectBroker(message)) # se elige el broker si es None, no se puede hacer nada

bandera = False
if(consumer.getBrokerId() != None):
    sleep(1)
    socket.send_pyobj([consumer.getBrokerId(),True]) # se manda activar del lado del broker seleccionado true
    sleep(1)
    topics = message = socket.recv_pyobj() # se recibe el diccionario de topicos del broker
    print(f"Consuming from broker {consumer.getBrokerId()} topics: {topics}")
else:
    bandera = True
    print("No hay brokers disponibles")

#  We create a new file with the topics in brokers
archivoHMTL = open('/home/alejandro/Sistemas_distribuidos/ProyectoFinal_Kafka/src/Consumer/templates/Buttons.html','w')
archivoHMTL.write('<!-- Archivo con los botones y las acciones que se ejecutarán -->\n')
#  Buttons
contador = 0
archivoHMTL.write('<div class="btn-group">')
for i in topics:
    archivoHMTL.write('<div class="dropdown">')
    archivoHMTL.write('\n\t<button class="btn btn-secondary dropdown-toggle" type="button" id="'+i+'" data-toggle="dropdown" aria-expanded="false" style="border-radius: 0px;">\n\t\t'+i+'\n\t</button>\n')
    archivoHMTL.write('\t<div class="dropdown-menu" aria-labelledby="'+i+'">')
    for j in topics[i]:
        contador += 1
        archivoHMTL.write('\n\t\t<button class="dropdown-item" data-toggle="modal" data-target="#exampleModal'+str(contador)+'">'+j+'</button>')
    archivoHMTL.write('\n\t</div>\n</div>\n')
archivoHMTL.write('</div>')
contador = 0
archivoHMTL.write('\n\n<!-- Modales -->')
for i in topics:
    for j in topics[i]:
        contador += 1 
        archivoHMTL.write('\n<div class="modal fade" id="exampleModal'+str(contador)+'" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"><div class="modal-dialog  modal-dialog-centered"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="exampleModalLabel">'+i+'</h5></div><div class="modal-body">Consumiendo el mensaje: '+j+'</div><div class="modal-footer"><button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button></div></div></div></div>')
archivoHMTL.close()

#  Run server
app = Flask(__name__, static_folder='templates')
if(bandera == False):
    @app.route('/',methods=['GET'])
    def home():
        return render_template('Consumer.html', topics = topics)
else:
    @app.route('/',methods=['GET'])
    def home():
        return render_template('Error500.html')
    
if __name__ == "__main__":
    app.run(debug=1,host='localhost', port = 8080)