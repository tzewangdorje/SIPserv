# twisted
from twisted.trial import unittest
# sipServ
from ..binding import Binding, BindingApiMemory


class MessageTestCase(unittest.TestCase):

    def test_create_message_from_udp_datagram(self):
        user = "sip:test@sipserv.org"
        endPoint = "sip:test@192.168.1.108"
        binding = Binding(endPoint, 3600)
        
        bam = BindingApiMemory()
        self.assertEqual(0, len(bam.getUsers()))
        bam.addUser(user)
        self.assertEqual(1, len(bam.getUsers()))
        bam.addBinding(user, binding)
        bindings = bam.getBindings(user)        
        self.assertEqual(1, len(bindings))
        self.assertEqual(bindings[endPoint].name, endPoint)
        self.assertEqual(bindings[endPoint].expires, 3600)
        bam.deleteUser(user)
        self.assertEqual(0, len(bam.getUsers()))
        self.assertRaises(KeyError, bam.getBindings, user)
        
        
                
            
    