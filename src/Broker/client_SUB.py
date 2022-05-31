#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import sys
from time import sleep
from flask import jsonify
from random import seed
from random import randint
sys.path.insert(0,'C:/Users/PC/Desktop/8voSemestre/Sistemas distribuidos/ProyectoFinal_Kafka\src/tools')
from ProducerConsumer import *
seed(1)
context = zmq.Context()
consumer = Consumer()
#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")


def selectBroker(message):
    if message[1] and message[2]: # si ambos brokers estan ocupados regresa None
        return None
    if message[2]: # si el broker 2 esta ocupado regresa 1
        return 1
    if message[1]: # si el broker 1 esta ocupado regresa 2
        return 2
    
    return randint(1,2)

# se envia una peticion de modo consume
sleep(1)
socket.send_pyobj({'mode':'consume'})

consumer.setConsumingStatus(True) # se cambia el estado del conusmer a activo, es decir, esta consumiendo
sleep(1)
message = socket.recv_pyobj() # se recibe un diccionario {1:<estado>,2:<estado>}
consumer.setBrokerId(selectBroker(message)) # se elige el broker si es None, no se puede hacer nada

if(consumer.getBrokerId() != None):
    sleep(1)
    socket.send_pyobj([consumer.getBrokerId(),True]) # se manda activar del lado del broker seleccionado true
    sleep(1)
    topics = message = socket.recv_pyobj() # se recibe el diccionario de topicos del broker
    print(f"Consuming from broker {consumer.getBrokerId()} topics: {topics}")
else:
    print("No hay brokers disponibles")

