#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

from ast import Try
import zmq
import sys
sys.path.insert(0,'C:/Users/PC/Desktop/8voSemestre/Sistemas distribuidos/ProyectoFinal_Kafka\src/tools')
from ProducerConsumer import *

brokers = {
        1:Broker(broker_id = 1),
        2:Broker(broker_id = 2)
    }
initialCharge = {
    'Hola mundo': ['mensaje 1','mensaje 2', 'mensaje 3'],
    'Hello world': ['message 1', 'message 2', 'message 3'],
    'Hallo welt': ['botschaft 1', 'botschaft 2', 'botschaft 3'],
    'Ciao mondo': ['messaggio 1', 'messaggio 2', 'messaggio 3']
}
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")
# socket.setsockopt_string(zmq.SUBSCRIBE, '')

# funcion que permite recibir de los publishers {topic,message}
def PUB(message):
    socket.send_string("Recieved a message") # se notifica al publisher que recibio la peticion
    # se cambia el estado de los brokers a activo para que ningun otro cliente pueda conectarse
    brokers[1].setActiveStatus(True) 
    brokers[2].setActiveStatus(True)
    print("Publish mode")
    
    # si el mensaje es distinto a None se agregan los mensajes a cada broker
    if(message != None):
        brokers[1].addNewMessage(message['message'][0],message['message'][1]) 
        brokers[2].addNewMessage(message['message'][0],message['message'][1])
            
        print(f"Broker 1: {brokers[1].getTopics()}\n")
        print(f"Broker 2: {brokers[2].getTopics()}\n")
    else:
        print("waiting a message")    

# mensaje que permite mandar los topics a un consumer en especifico
def SUB():
    print("Consume mode\n")
    # despues de recibir el modo, se envia como respuesta un diccionario cuyas llaves son los id's de los brokers por lo tanto sus respectivos
    # valores seran su estado de actividad (activo o no activo)
    socket.send_pyobj({
                        1:brokers[1].getActiveStatus(),
                        2:brokers[2].getActiveStatus()
                    })
    message = socket.recv_pyobj() # se recibe una lista de dos elementos del cliente consumer donde el primer elemento es el ID del broker que selecciono el consumer y el segundo valor un booleano para indicar que ese broker estara activo y por lo tanto ocupado
    BrokerIdSelected = message[0] # se guarda este ID del broker elegido
    brokers[BrokerIdSelected].setActiveStatus(message[1]) # se activa el broker elegido
    socket.send_pyobj(brokers[BrokerIdSelected].getTopics()) # se envia como respuesta los topicos del broker seleccionado

# variable que indica si se recibe o no algun valor, en caso de que si se recibe algo entonces se inicializa con una carga inicial de topicos en los brokers con la finalidad de no ejecutar el cliente publisher e directo con la ejecucion del cliente consumer 
try:
    a = sys.argv[1]
    loadInitialCharge = True 
except:
    loadInitialCharge = False 

if __name__ == '__main__':
    while True:
        print("waiting for a message\n")
        # se descoupan ambos brokers
        brokers[1].setActiveStatus(False)
        brokers[2].setActiveStatus(False)
        # modo con carga inicial, se salta la ejecucion del publisher y solo se ejecuta el consumer
        if loadInitialCharge:
            # se le da la carga inicial tanto al broker uno como al dos
            brokers[1].setTopics(initialCharge)
            brokers[2].setTopics(initialCharge)
            print("initial charge loaded\n")
            # se recibe el mensaje del cliente consumer, se espera un diccionario con un solo par de llave (mode) y valor (consume)
            message = socket.recv_pyobj()
            if(message['mode']=='consume'):
                SUB() # se manda a llamar la funcion que permite comunicarse con un cliente de tipo consumer
            else:
                print("Error, wrong mode") # solo se acepta el diccionario {'mode':'conume'}
        else: # si no se recibe ningun argumento desde la ejecucion de este server, entonces se procede a realizar el Pipeline que se propone para para el buen funcionamiento del proyecto
            # Publisher => brokers => Consumer
            message = socket.recv_pyobj() # se recibe el mismo diccionario pero ahora se acepta ya sea publish o consume, en caso contrario no se podra comunicar con ningun cliente
            if(message['mode']=='publish'): # si se recibe un publish, entonces se manda a llamar la funcion que nos permite recibir info. del cliente publisher
                PUB(message)
            elif(message['mode']=='consume'): # si se recibe un consume, entonces se manda a llamar la funcion que nos permite mandar info. al cliente consumer
                SUB()
            else:
                print("Error, wrong mode")