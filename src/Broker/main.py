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
from ProducerConsumer import *

b1 = [Broker(broker_id = 1), Broker(broker_id = 1)]
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, '')

listener = 0
while True:
    #  Wait for next request from 
    print("waiting for a message\n")
    b1[0].setActiveStatus(False)
    b1[1].setActiveStatus(False)
    message = socket.recv_pyobj()
    if(message['mode']=='publish'):
        b1[0].setActiveStatus(True)
        b1[1].setActiveStatus(True)
        print("Publish mode")
        if(message != None):
            b1[0].addNewMessage(message['message'][0],message['message'][1])
            b1[1].addNewMessage(message['message'][0],message['message'][1])
                
            print(f"Broker 1: {b1[0].getTopics()}\n")
            print(f"Broker 2: {b1[1].getTopics()}\n")
        else:
            print("waiting a message")
    elif(message['mode']=='consume'):
        print("Consume mode\n")
        