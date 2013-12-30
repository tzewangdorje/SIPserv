from transaction import TransactionUser
from error import SipError


class UserAgent(TransactionUser):
    
    def __init__(self, transaction):
        self._transaction = transaction
        self.messageFactory = None    
    
    def process(self):
        try:
            self._inspectMethod()
            self._inspectHeader()
            self._processContent()
            self._applyExtensions()
            self._processRequest()
            return self._transaction
        except SipError, e:
            outMessage = self._getMsgFromErr(e, self._inMessage)
            self._outMessages.append(outMessage)
    
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
    
    def _register(self):
        message = self.messageFactory.makeResponse(200, 'OK', self._transaction.request, headers=[])
        self._transaction.addResponse(message)
    
    def _options(self):
        print "OPTIONS"
    
    def _invite(self):
        print "INVITE"
    
    def _bye(self):
        print "BYE"
    
            
class UserAgentClient(UserAgent):
    pass


class UserAgentServer(UserAgent):
    pass