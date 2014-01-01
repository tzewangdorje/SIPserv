# core
import traceback, random, re
from collections import OrderedDict
# sipServ
from header import HeaderField
from userAgent import UserAgentServer

class Message(object):
                   
    def __init__(self, data=None):
        self.indentifier = None
        self.request = None
        self.final = None
        self.header = OrderedDict()
        self.body = ""
        self.sent = False
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
        for key,field in self.header.iteritems():
            ret = ret + field.write() + "\r\n"
        ret = ret + "\r\n"
        ret = ret + self.body
        return ret
    
    def _parse(self, data):
        headerDone = False
        start = True
        lines = data.splitlines()
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
                    key = headerField.name.lower()
                    self.header[key] = headerField
                except: # this header field already exists, so add values to the existing one, TO DO
                    # header[hf.name].append(hf)
                    print traceback.format_exc()       
    
    def _validate(self):
        return True
    
    def getUserAgent(self):
        return UserAgentServer()
    
    def isRequest(self):
        return self.request
    
    def isResponse(self):
        return not self.request
    
    def isProvisional(self):
        return not self.request and not self.final
    
    def isFinal(self):
        return not self.request and self.final
        
    def getId(self):
        try:
            return self.header["via"].values[0].params["branch"]
        except:
            return None
    
    
class MessageRequest(Message):
    
    def __init__(self, data):
        Message.__init__(self, data)
        self.request = True
        self.requestUri = self.start_line.split(" ")[1]
        
    @property
    def addressOfRecord(self):
        to = self.header["to"].values[0].value
        m = re.search(r"<(.+)>", to)
        return m.group(1)
    
    def getReturnIp(self):
        via = self.header["via"]
        return via.values[0].value.split(" ")[1]
    
    def getReturnPort(self):
        via = self.header["via"]
        if via.values[0].params["rport"].isdigit():
            return via.values[0].params["rport"]
        else:
            return "5060"
    
    def getReturnTransport(self):
        via = self.header["via"]
        return via.values[0].value.split(" ")[0].split("/")[2]


class MessageResponse(Message):

    @property
    def start_line(self):
        return "SIP/2.0 "+self.code+" "+self.reasonPhrase
    
    def __init__(self, data):
        Message.__init__(self, data)
        self.request = False
        self.code = ""
        self.reasonPhrase = ""
    
    def configureByRequest(self, requestMessage):
        self.returnIp = requestMessage.getReturnIp()
        self.returnPort = requestMessage.getReturnPort()
        self.returnTransport = requestMessage.getReturnTransport()
        self.header["via"] = requestMessage.header["via"]
        toField = requestMessage.header["to"]
        try:
            toField.values[0].params["tag"]
        except KeyError:
            # no dialog tag yet - add one
            toField.values[0].params["tag"] = '%x' % random.randint(0,2**31)
        self.header["to"] = toField
        self.header["from"] = requestMessage.header["from"]
        self.header["call-id"] = requestMessage.header["call-id"]
        self.header["cseq"] = requestMessage.header["cseq"]


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
        self.final = False
    
        
class MessageResponseSuccess(MessageResponse):
    
    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "SUCCESS"
        self.final = True
    
        
class MessageResponseRedirect(MessageResponse):
    
    def __init__(self, data=None):
        MessageResponse.__init__(self, data)
        self.identifier = "REDIRECT"
        self.final = True   


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
        
        