#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import sys
from time import sleep
from flask import jsonify
sys.path.insert(0,'C:/Users/PC/Desktop/8voSemestre/Sistemas distribuidos/ProyectoFinal_Kafka\src/tools')
from ProducerConsumer import *

context = zmq.Context()
b1 = Broker()
#  Socket to talk to server
print("Connecting to the brokers …")
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:5555")



sleep(1)
socket.send_pyobj({'mode':'publish','message':('hello world','message 1')})
sleep(1)
socket.send_pyobj({'mode':'publish','message':('hello world','message 2')})
sleep(1)
socket.send_pyobj({'mode':'publish','message':('qwerty','message 2')})

print("message sent to brokers")


