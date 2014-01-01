# core
import traceback
# sipServ
from message import MessageRequestRegister, MessageRequestInvite
from message import MessageResponseProvisional, MessageResponseSuccess, MessageResponseRedirect
from message import MessageResponseClientError, MessageResponseServerError, MessageResponseGlobalFailure 
from userAgent import UserAgentClient, UserAgentServer

class MessageFactory(object):
    
    def __init__(self):
        self._methodHash = {
            "REGISTER": MessageRequestRegister, 
            "INVITE": MessageRequestInvite, 
        }
        self._codeHash = {
            "1": MessageResponseProvisional, 
            "2": MessageResponseSuccess, 
            "3": MessageResponseRedirect, 
            "4": MessageResponseClientError, 
            "5": MessageResponseServerError, 
            "6": MessageResponseGlobalFailure, 
        }
        
    def createFromDatagram(self, data):
        lines = data.splitlines()
        messageType = lines[0].split(" ", 1)[0]
        try:
            return self._methodHash[messageType](data)
        except KeyError:
            print "Sorry, message type not supported."
            
    def makeRequest(self,method):
        pass
    
    def makeResponse(self, code, reasonPhrase, requestMessage, headers):
        code = str(code)
        message = self._codeHash[code[0]]()
        message.code = code
        message.reasonPhrase = reasonPhrase
        message.configureByRequest(requestMessage)
        for headerField in headers:
            message.header[headerField.name] = headerField
        return message

    
class TransactionUserFactory(object):

    def __init__(self, messageFactory):
        self._messageFactory = messageFactory
    
    def create(self, message, transaction):
        if message.isRequest():
            userAgent = UserAgentServer(transaction)
        else:
            userAgent = UserAgentClient(transaction)
        userAgent.messageFactory = self._messageFactory
        return userAgent

        