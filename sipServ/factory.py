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
        lines = data.split("\r\n")
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
        for header in headers:
            message.headers.append(header)
        message.configureByRequest(requestMessage)
        return message

    
class TransactionUserFactory(object):

    def __init__(self, messageFactory):
        self._messageFactory = messageFactory
    
    def create(self, transaction):
        message = transaction.message
        if message.isRequest():
            userAgent = UserAgentServer(message)
        else:
            userAgent = UserAgentClient(message)
        userAgent.messageFactory = self._messageFactory
        return userAgent

        