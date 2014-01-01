# core
import traceback, re
# sipServ
from error import SipError
from binding import get_binding_api, Binding
from header import HeaderField, HeaderFieldValue

class TransactionUser(object):
    
    def __init__(self, transaction):
        self._transaction = transaction
        self.messageFactory = None        

class UserAgent(TransactionUser):
    
    def __init__(self, transaction):
        TransactionUser.__init__(self, transaction)
  
    def process(self):
        try:
            self._inspectMethod()
            self._inspectHeader()
            self._processContent()
            self._applyExtensions()
            self._processRequest()
            return self._transaction
        except SipError, e:
            message = self._getMsgFromErr(e, self._transaction.request)
            self._transaction.addResponse(message)
            return self._transaction
    
    def getOutMessages(self):
        return self._outMessages
    
    def _getMsgFromErr(self, error, inMessage):
        message = self.messageFactory.makeResponse(error.code, error.message, inMessage, error.headers)
        return message
    
    def _inspectMethod(self):
        pass
    
    def _inspectHeader(self):
        self._processToAndRequestUri()
        self._mergeRequests()
        self._require()
    
    def _processToAndRequestUri(self):
        pass
    
    def _mergeRequests(self):
        pass
    
    def _require(self):
        pass
    
    def _processContent(self):
        pass
    
    def _applyExtensions(self):
        pass
    
    def _processRequest(self):
        if self._transaction.request.identifier=="REGISTER":
            self._register()
        elif self._transaction.request.identifier=="OPTIONS":
            self._options()
        elif self._transaction.request.identifier=="INVITE":
            self._invite()
        elif self._transaction.request.identifier=="BYE":
            self._bye()
        else:
            raise SipError(405, 'Method Not Allowed')
    
            
class UserAgentClient(UserAgent):
    
    def __init__(self, transaction):
        UserAgent.__init__(self, transaction)
        self._bindApi = BindingApiMemory()


class UserAgentServer(UserAgent):
    
    def __init__(self, transaction):
        UserAgent.__init__(self, transaction)
        self._bindApi = get_binding_api()
        
    def _register(self):
        # can this server handle this registration? If not, forward on
        if not self._myDomain(self._transaction.request.requestUri):
            return self._proxyRequest()
        # now we need to authenticate the sip endpoint
        if self._requiresAuth():
            raise SipError(401, 'Unauthorized')
        elif self._badAuth():
            raise SipError(403, 'Forbidden')
        # let's do a lookup now to see if we know this user
        aOR = self._transaction.request.addressOfRecord
        try:
            requestContact = self._transaction.request.header["contact"]
        except:
            requestContact = None
        # it is not required to pass a contact, but if it is passed, then update the bindings
        if requestContact: 
            sipUri = requestContact.values[0].value
            expires = requestContact.values[0].params["expires"]
            m = re.search(r"<(.+)>", sipUri)
            endPoint = m.group(1)
            newBinding = Binding(endPoint, expires)
            try:
                self._bindApi.addBinding(aOR, newBinding)
            except KeyError:    
                raise SipError(404, 'Not Found')            
        try:
            bindings = self._bindApi.getBindings(aOR)
        except KeyError:    
            raise SipError(404, 'Not Found')
        contact = HeaderField()
        contact.name = "Contact"
        for key, binding in bindings.iteritems():
            hfv = HeaderFieldValue()
            hfv.value = "<"+binding.name+">"
            hfv.params["expires"] = binding.expires
            contact.values.append(hfv)
        message = self.messageFactory.makeResponse(200, 'OK', self._transaction.request, headers=[contact])
        self._transaction.addResponse(message)
        
    def _options(self):
        print "OPTIONS"
    
    def _invite(self):
        print "INVITE"
    
    def _bye(self):
        print "BYE"
        
    def _myDomain(self, requestUri):
        return True
    
    def _proxyRequest(self):
        pass
    
    def _requiresAuth(self):
        return False
    
    def _badAuth(self):
        return False