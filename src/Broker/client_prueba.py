#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import sys
from flask import jsonify
sys.path.insert(0,'C:/Users/PC/Desktop/8voSemestre/Sistemas distribuidos/ProyectoFinal_Kafka\src/tools')
print(sys.path)
from ProducerConsumer import *

context = zmq.Context()
b1 = Broker()
#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
# for request in range(10):
print(f"Sending request…")
socket.send(f"{jsonify(b1)}")

#  Get the reply.
message = socket.recv()
print(f"Received reply [ {message} ]")

