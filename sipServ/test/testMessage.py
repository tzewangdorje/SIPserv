# twisted
from twisted.trial import unittest
# sipServ
from ..factory import MessageFactory
from ..message import Message


datagram1 = """REGISTER sip:sipserv.org SIP/2.0
Via: SIP/2.0/UDP 127.0.0.1;rport;branch=z9hG4bKqbgsgzca
Max-Forwards: 70
To: "Test" <sip:test@127.0.0.1>
From: "Test" <sip:test@127.0.0.1>;tag=gcwta
Call-ID: wwkjsurswesebgl@hostname
CSeq: 638 REGISTER
Contact: <sip:test@127.0.0.1>;expires=3600
Allow: INVITE,ACK,BYE,CANCEL,OPTIONS,PRACK,REFER,NOTIFY,SUBSCRIBE,INFO,MESSAGE
User-Agent: Testing/1.0.0
Content-Length: 0
"""


class MessageTestCase(unittest.TestCase):

    def test_create_message_from_udp_datagram(self):
        messageFactory = MessageFactory()
        message = messageFactory.createFromDatagram(datagram1)
        self.assertEqual(message.request, True)
        self.assertEqual(message.identifier, "REGISTER")
        self.assertEqual(message.requestUri, "sip:sipserv.org")
        self.assertEqual(type(message.header["via"]).__name__, "HeaderField")
        self.assertEqual(type(message.header["to"]).__name__, "HeaderField")
        self.assertEqual(message.header["to"].values[0].value, '"Test" <sip:test@127.0.0.1>')
        self.assertEqual(message.addressOfRecord, "sip:test@127.0.0.1")
        
                
            
    