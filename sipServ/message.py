# core
import traceback, random
# sipServ
from header import HeaderField
from userAgent import UserAgentServer

class Message(object):
                   
    def __init__(self, data=None):
        self.indentifier = None
        self.request = None
        self.header = []
        self._headerLookup = {}
        self.body = ""
        if data:
            self._parse(data)
        if not self._validate():
            raise Exception('Invalid Message format')
    
    def __repr__(self):
        ret = "{\n"
        ret = ret+"  'StartLine': '"+self.start_line+"',\n"
        ret = ret+"  'Header': {\n"
        for field in self.header:
            ret = ret+"    '"+field.name+"': {\n"
            for value in field.values:
                ret = ret+"      "+str(value)+",\n"
        ret = ret+"    },\n"
        ret = ret+"  'Body': '"+self.body+"'\n"
        ret = ret+"}\n"
        return ret
    
    def write(self):
        ret = self.start_line + "\r\n"
        for field in self.header:
            ret = ret + field.write() + "\r\n"
        ret = ret + "\r\n"
        ret = ret + self.body
        return ret
    
    def _parse(self, data):
        headerDone = False
        start = True
        lines = data.split("\r\n")
        for line in lines:
            if start:
                self.start_line = line
                start = False
            elif line=="":
                headerDone = True
            elif headerDone:
                self.body = self.body+line
            else:
                headerField = HeaderField(line)
                try:
                    self.addHeaderField(headerField)
                except: # this header field already exists, so add values to the existing one
                    # header[hf.name].append(hf)
                    print traceback.format_exc()       
    
    def _validate(self):
        return True
    
    def getHeaderField(self, name):
        lowerKey = name.lower()
        try:
            return self._headerLookup[lowerKey]
        except:
            return False
    
    def getUserAgent(self):
        return UserAgentServer()
    
    def isRequest(self):
        return self._request
    
    def isResponse(self):
        return not self._request
    
    def addHeaderField(self, headerField):
        lowerKey = headerField.name.lower()
        self._headerLookup[lowerKey] = headerField
        self.header.append(headerField)
    
    
class MessageRequest(Message):
    
    def __init__(self, data):
        Message.__init__(self, data)
        self._request = True
    
    def getReturnIp(self):
        via = self.getHeaderField("via")
        return via.values[0].value.split(" ")[1]
    
    def getReturnPort(self):
        via = self.getHeaderField("via")
        if via.values[0].params["rport"].isdigit():
            return via.values[0].params["rport"]
        else:
            return "5060"
    
    def getReturnTransport(self):
        via = self.getHeaderField("via")
        return via.values[0].value.split(" ")[0].split("/")[2]


class MessageResponse(Message):

    @property
    def start_line(self):
        return "SIP/2.0 "+self.code+" "+self.reasonPhrase
    
    def __init__(self, data):
        Message.__init__(self, data)
        self._request = False
        self.code = ""
        self.reasonPhrase = ""
    
    def configureByRequest(self, requestMessage):
        self._requestMessage = requestMessage
        self.returnIp = self._requestMessage.getReturnIp()
        self.returnPort = self._requestMessage.getReturnPort()
        self.returnTransport = self._requestMessage.getReturnTransport()
        self.header.append( requestMessage.getHeaderField("via") )
        toField = requestMessage.getHeaderField("to")
        try:
            toField.values[0].params["tag"]
        except KeyError:
            # no dialog tag yet - add one
            toField.values[0].params["tag"] = '%x' % random.randint(0,2**31)
        self.header.append( toField )
        self.header.append( requestMessage.getHeaderField("from") )
        self.header.append( requestMessage.getHeaderField("call-id") )
        self.header.append( requestMessage.getHeaderField("cseq") )


class MessageRequestRegister(MessageRequest):

    def __init__(self, data=None):
        MessageRequest.__init__(self, data)
        self.identifier = "REGISTER"

        
class MessageRequestInvite(MessageRequest):
    
    def __init__(self, data=None):
        MessageRequest.__init__(self, data)
        self.identifier = "INVITE"

        
class MessageResponseProvisional(MessageResponse):
    
    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "PROVISIONAL"
    
        
class MessageResponseSuccess(MessageResponse):
    
    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "SUCCESS"
    
        
class MessageResponseRedirect(MessageResponse):
    
    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "REDIRECT"    


class MessageResponseClientError(MessageResponse):

    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "CLIENT_ERROR"
    
    def configureByRequest(self, requestMessage):
        MessageResponse.configureByRequest(self, requestMessage)
        if self.code=="405":
            self.header.append( HeaderField("Allow: INVITE,ACK,BYE,CANCEL,OPTIONS") ) # INVITE missing for testing!
    
        
class MessageResponseServerError(MessageResponse):
    
    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "SERVER_ERROR"
    
        
class MessageResponseGlobalFailure(MessageResponse):
    
    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "GLOBAL_FAILURE"
        
        