class TransactionLayer(object):
    
    def __init__(self, stateMachine):
        self._stateMachine = stateMachine
    
    def getTransaction(self, message):
        transaction = self._stateMachine.lookup(message)
        if transaction:
            return transaction
        else:
            transaction = self._create(message)
            self._stateMachine.store(transaction)
            return transaction
    
    def _create(self, message):
        if message.isRequest():
            return TransactionServer(message)
        else:
            return TransactionClient(message)          


class Transaction(object):
    
    def __init__(self, message, ip="127.0.0.1", port="5060", protocol="udp"):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.message = message
        self.state = None
        # request
        self.request = None
        # responses
        self.provisionals = []
        self.finals = []


class TransactionClient(Transaction):
    
    def __init__(self, message):
        Transaction.__init__(self, message)


class TransactionClientInvite(TransactionClient):
    
    # calling -> proceeding -> completed -> terminated
    def __init__(self, message):
        TransactionClient.__init__(self, message)
        self.state = "calling"


class TransactionClientNonInvite(TransactionClient):
    
    # trying -> proceeding -> completed -> terminated
    def __init__(self, message):
        TransactionClient.__init__(self, message)
        self.state = "trying"


class TransactionServer(Transaction):
    
    def __init__(self, message):
        Transaction.__init__(self, message)


class TransactionServerInvite(TransactionServer):
    
    def __init__(self, message):
        # proceeding -> completed -> confirmed -> terminated
        TransactionServer.__init__(self, message)
        self.state = "proceeding"


class TransactionServerNonInvite(TransactionServer):
    
    def __init__(self, message):
        # trying -> proceeding -> completed -> terminated
        TransactionServer.__init__(self, message)
        self.state = "proceeding"


class TransactionUser(object):
    pass

