class PersistenceApi(object):
    
    def __init__(self):
        pass
    
    def lookup(self, message):
        pass
    
    def store(self, transaction):
        pass
    
class PersistenceApiMemory(PersistenceApi):

    def __init__(self):
        PersistenceApi.__init__(self)
        self._store = {}
        
    def lookup(self, message):
        id = message.getId()
        try:
            return self._store[id]
        except KeyError:
            return False
        
    def store(self, transaction):
        id = transaction.message.getId()
        try:
            self._store[id]
        except KeyError:
            self._store[id] = transaction
        
        