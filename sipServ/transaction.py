class TransactionLayer(object):
    
    def __init__(self, persistenceApi):
        self._persistenceApi = persistenceApi
    
    def getTransaction(self, message):
        transaction = self._persistenceApi.lookup(message)
        if transaction:
            return transaction
        else:
            transaction = self._create(message)
            self._persistenceApi.store(transaction)
            return transaction
    
    def _create(self, message):
        if message.isRequest():
            transaction = TransactionServer()
            message.sent = True
            transaction.addRequest(message)
        else:
            transaction = TransactionClient()
            transaction.addResponse(message)
        return transaction      


class Transaction(object):
    
    def __init__(self, ip="127.0.0.1", port="5060", protocol="udp"):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.state = None
        # request
        self.request = None
        # responses
        self.provisionals = []
        self.finals = []
        
    def getId(self):
        return self.request.getId()
    
    def addResponse(self, message):
        if message.isFinal():
            self.finals.append(message)
        elif message.isProvisional():
            self.provisionals.append(message)
            
    def addRequest(self, message):
        self.request = message
            
    def getOutMessages(self):
        messages = []
        if not self.request.sent:
            self.request.sent = True
            messages.append(self.request)
        for message in self.provisionals:
            if not message.sent:
                message.sent = False
                messages.append(message)
        for message in self.finals:
            if not message.sent:
                message.sent = False
                messages.append(message)
        return messages


class TransactionClient(Transaction):
    
    def __init__(self, ip="127.0.0.1", port="5060", protocol="udp"):
        Transaction.__init__(self, ip="127.0.0.1", port="5060", protocol="udp")


class TransactionClientInvite(TransactionClient):
    
    # calling -> proceeding -> completed -> terminated
    def __init__(self, ip="127.0.0.1", port="5060", protocol="udp"):
        TransactionClient.__init__(self, ip="127.0.0.1", port="5060", protocol="udp")
        self.state = "calling"


class TransactionClientNonInvite(TransactionClient):
    
    # trying -> proceeding -> completed -> terminated
    def __init__(self, ip="127.0.0.1", port="5060", protocol="udp"):
        TransactionClient.__init__(self, ip="127.0.0.1", port="5060", protocol="udp")
        self.state = "trying"


class TransactionServer(Transaction):
    
    def __init__(self, ip="127.0.0.1", port="5060", protocol="udp"):
        Transaction.__init__(self, ip="127.0.0.1", port="5060", protocol="udp")


class TransactionServerInvite(TransactionServer):
    
    def __init__(self, ip="127.0.0.1", port="5060", protocol="udp"):
        # proceeding -> completed -> confirmed -> terminated
        TransactionServer.__init__(self, ip="127.0.0.1", port="5060", protocol="udp")
        self.state = "proceeding"


class TransactionServerNonInvite(TransactionServer):
    
    def __init__(self, ip="127.0.0.1", port="5060", protocol="udp"):
        # trying -> proceeding -> completed -> terminated
        TransactionServer.__init__(self, ip="127.0.0.1", port="5060", protocol="udp")
        self.state = "proceeding"

