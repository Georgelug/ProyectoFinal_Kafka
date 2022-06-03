# Broker
class Broker:
    def __init__(self, active_status=False, broker_id = 0):
        self.topics = {}
        self.broker_id = broker_id
        self.active_status = active_status
    
    # setters and getters
    # del lado del cosumer
    def getActiveStatus(self): # obtiene el status del broker, ocupado o desocupado, esta funcion es para el consumer
        return self.active_status 
    def setActiveStatus(self,active_status = True): # cambia el status del broker, ocupado o desocupado, esta funcion es para el consumer
        self.active_status = active_status
    def getBrokerId(self): # obtienes el id del broker, solo hay 1 y 2
        return self.broker_id
    def getTopics(self): # funcion que devuelve el diccionario de topics, IMPORTANTE 
        return self.topics
    def getTopic_toClient(self,key):  # funcion que muestra los mensajes de un topic
        return self.getTopics()[key]
    def getMessage(self,key,indexMessage = 0): # funcion que obtiene el string o mensaje que el usuario o consumer elige
        return self.getTopics()[key][indexMessage]
    
    # carga inicial (opcional)
    def setTopics(self, topics): # funcion que modifica el diccionario, esta servira para realizar cargas iniciales
        self.topics = topics
    
    # del lado del producer
    def addNewMessage(self, topic, message): # funcion que agrega un nuevo mensaje desde el producer, recibe un topico y un mensaje, en caso de que no exista el topico, entonces se crea la llave del diccionario y el mensaje  
        try:
            self.topics[topic].append(message)
        except:
            self.topics[topic] = [message]
            
# Client
class Client:
    def __init__(self,client_id = 0):
        self.client_id = client_id
    # setters and getters
    def getClienId(self):
        return self.client_id
    def setClientId(self, client_id):
        self.client_id = client_id
    def getTopicsFromBroker(self, broker_id):
        return self.listOfBrokers[broker_id].getTopics()

class Producer(Client):
    def __init__(self,client_id = 0):
        super().__init__(self,client_id)
        self.listOfBrokers = {
                                1: Broker(broker_id = 1), 
                                2: Broker(broker_id = 2)
                            }
    # nota agregar un metodo que obtenga lista de brokers con info de los servers
    # Producer methods
    
    def produce(self, broker_id, key, message):
        self.listOfBrokers[broker_id].addNewMessage(key,message)
        return self.listOfBrokers[broker_id].getTopics()
    def deleteMessage(self, broker_id, key, indexMessage):
        self.listOfBrokers[broker_id].deleteMessage(key,indexMessage)
        return self.listOfBrokers[broker_id].getTopics()
    def setMessage(self, broker_id, key, indexMessage,message):
        self.listOfBrokers[broker_id].setMessage(key,indexMessage,message)
        return self.listOfBrokers[broker_id].getTopics()
    
class Consumer(Client):
    def __init__(self,client_id = 0,consuming_status = False, topic_id = 1, broker_id = 1):
        super().__init__()
        self.consuming_status = consuming_status
        self.topic_id = topic_id
        self.broker_id = broker_id
        self.message = None
    # getters and setters
    def setBrokerId(self, broker_id):
        self.broker_id = broker_id
    def getBrokerId(self):
        return self.broker_id
    def setConsumingStatus(self, status):
        self.consuming_status = status
    def getConsumingStatus(self):
        return self.consuming_status
    def setTopicId(self,topic_id):
        self.topic_id = topic_id
    def getTopicId(self):
        return self.topic_id
    def setMessage(self, message):
        self.message = message
    def getMessage(self):
        return self.message
    
    # Consumer methods
    def getTopic(self,key):
        return self.listOfBrokers[self.broker_id].getTopic(key)
    def consume(self,key,indexMessage):
        self.setMessage(self.listOfBrokers[self.broker_id].getMessage(key,indexMessage))
        
        
    
