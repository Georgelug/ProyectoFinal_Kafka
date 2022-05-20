# Broker
class Broker:
    def __init__(self, active_status=False,broker_id = 0):
        self.topics = {}
        self.broker_id = broker_id
        self.active_status = active_status
    
    # setters and getters
    def getActiveStatus(self):
        return self.active_status
    def setActiveStatus(self, status):
        self.active_status = status
    def getBrokerId(self):
        return self.broker_id
    def setBrokerId(self, broker_id):
        return self.broker_id
    def getTopics(self):
        return self.topics
    def setTopics(self, topics):
        self.topics = topics
    
    # other methods
    def getTopic(self,key):
        return self.getTopics()[key]
    def getMessage(self,key,indexMessage = 0):
        return self.getTopics()[key][indexMessage]
    def deleteMessage(self,key,indexMessage):
        self.topics[key].pop(indexMessage)
    def setMessage(self,key,indexMessage,message):
        self.topics[key][indexMessage] = message
    def addNewMessage(self, key, message):
        self.topics[key].append(message)
        
# Client
class Client:
    def __init__(self,client_id = 0):
        self.client_id = client_id
    # setters and getters
    def getClienId(self):
        return self.client_id
    def setClientId(self, client_id):
        self.client_id = client_id

class Producer(Client):
    def __init__(self,client_id = 0):
        super().__init__(self,client_id)
        self.listOfBrokers = {
                                1: Broker(broker_id = 1), 
                                2: Broker(broker_id = 2)
                            }
    # nota agregar un metodo que obtenga lista de brokers con info de los servers
    # Producer methods
    def getTopicsFromBroker(self, broker_id):
        return self.listOfBrokers[broker_id].getTopics()
    def publish(self, broker_id, key, message):
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
        super().__init__(self,client_id)
        self.listOfBrokers = {1: Broker(broker_id = 1), 2: Broker(broker_id = 2)}
        self.consuming_status = consuming_status
        self.topic_id = topic_id
        self.broker_id = broker_id
        self.message = None
    
    