#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import sys
from flask import jsonify
sys.path.insert(0,'C:/Users/PC/Desktop/8voSemestre/Sistemas distribuidos/ProyectoFinal_Kafka\src/tools')
print(sys.path)
from ProducerConsumer import *

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

b1 = Broker()

while True:
    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")
    #  Do some 'work'
    time.sleep(1)
    #  Send reply back to client
    socket.send(b"objeto recibido")