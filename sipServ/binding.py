from collections import OrderedDict


class Binding(object):
    
    def __init__(self, name, expires):
        self.name = name
        self.expires = expires
        

class BindingApi(object):
    
    def __init__(self):
        pass
    
    def getUsers(self):
        pass
    
    def addUser(self, user):
        pass
    
    def deleteUser(self, user):
        pass
    
    def getBindings(self, user):
        pass
    
    def clearBindings(self, user):
        pass
    
    def addBinding(self, user, binding):
        pass
    
    
class BindingApiMemory(BindingApi):
    
    def __init__(self):
        BindingApi.__init__(self)
        self._store = {}
        self._store["sip:test@127.0.0.1"] = OrderedDict() # REMOVE THIS HARD_CODED TEST USER !!!
        
    def getUsers(self):
        return self._store.keys()
    
    def addUser(self, user):
        self._store[user] = OrderedDict()

    def deleteUser(self, user):
        del self._store[user]
        
    def clearBindings(self, user):
        try:
            self._store[user] = OrderedDict() 
        except:
            pass
        
    def addBinding(self, user, binding):
        self._store[user][binding.name] = binding
        
    def getBindings(self, user):
        return self._store[user]
            
bindingApi = BindingApiMemory()
def get_binding_api():
    return bindingApi    