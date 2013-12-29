# core
import traceback
# twisted
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
# sipServ
from sipServ.factory import MessageFactory, TransactionUserFactory
from sipServ.transaction import TransactionLayer
from sipServ.state import StateMachine


class SipProtocol(DatagramProtocol):
    
    def startProtocol(self):
        self._stateMachine = StateMachine()
        self._messageFactory = MessageFactory()
        self._transactionLayer = TransactionLayer(self._stateMachine)
        self._tuFactory = TransactionUserFactory(self._messageFactory)
        # hack so I can start building, but needs writing properly
        host = "127.0.0.1"
        port = 5060
        self.transport.connect(host, port)
        print "Communicating with client on ip %s port %d" % (host, port)
    
    def datagramReceived(self, data, (host, port)):
        try:
            inMessage = self._messageFactory.createFromDatagram(data)
            packet = inMessage.write()
            print packet
            transaction = self._transactionLayer.getTransaction(inMessage)
            tu = self._tuFactory.create(transaction)
            tu.process()
            for outMessage in tu.getOutMessages():
                transaction = self._transactionLayer.getTransaction(outMessage)
                if transaction:
                    self._send(transaction)
        except:
            print traceback.format_exc()
    
    def connectionRefused(self): # Possibly invoked if there is no server listening on the address to which we are sending.
        print "No one listening"            
    
    def _send(self, transaction):
        message = transaction.message
        port = int(message.returnPort)
        ip = message.returnIp
        packet = message.write()
        print packet
        self.transport.write(packet, (ip, port))


reactor.listenUDP(5061, SipProtocol())
reactor.run()
