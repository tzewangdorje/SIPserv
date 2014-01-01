# twisted
from twisted.trial import unittest
# sipServ
from ..header import HeaderField, HeaderFieldValue

class HeaderTestCase(unittest.TestCase):

    def test_create_header_field_value(self):
        # simple
        value = "70"
        headerFieldValue = HeaderFieldValue(value)
        self.assertEqual(headerFieldValue.value, value)
        self.assertEqual(len(headerFieldValue.params), 0)
        # more complex
        value = "SIP/2.0/UDP 127.0.0.1;branch=z9hG4bKufswnhxy;rport"
        headerFieldValue = HeaderFieldValue(value)
        self.assertEqual(headerFieldValue.value, "SIP/2.0/UDP 127.0.0.1")
        self.assertEqual(len(headerFieldValue.params), 2)
        self.assertEqual(headerFieldValue.params["branch"], "z9hG4bKufswnhxy")
        self.assertEqual(headerFieldValue.params["rport"], "rport")
                
            
    def test_create_header_from_line(self):
        # simple
        line = "Max-Forwards: 70"
        headerField = HeaderField(line)
        self.assertEqual(line, headerField.write())
        self.assertEqual("70", headerField.values[0].value)
        self.assertEqual(0, len(headerField.values[0].params))
        # more complex
        line = "Via: SIP/2.0/UDP 127.0.0.1;branch=z9hG4bKufswnhxy;rport"
        headerField = HeaderField(line)
        self.assertEqual(line, headerField.write())
        self.assertEqual(1, len(headerField.values))
        self.assertEqual("SIP/2.0/UDP 127.0.0.1", headerField.values[0].value)
        self.assertEqual(2, len(headerField.values[0].params))
        self.assertEqual("z9hG4bKufswnhxy", headerField.values[0].params["branch"])
        self.assertEqual("rport", headerField.values[0].params["rport"])
        # multiple values
        line = "Allow: INVITE,ACK,BYE,CANCEL,OPTIONS,PRACK,REFER,NOTIFY,SUBSCRIBE,INFO,MESSAGE"
        headerField = HeaderField(line)
        self.assertEqual(line, headerField.write())
        self.assertEqual(11, len(headerField.values))
        self.assertEqual("INVITE", str(headerField.values[0]))
        self.assertEqual("HeaderFieldValue", type(headerField.values[0]).__name__)
        self.assertEqual(0, len(headerField.values[0].params))
        self.assertEqual("ACK", str(headerField.values[1]))
        self.assertEqual("HeaderFieldValue", type(headerField.values[1]).__name__)
        self.assertEqual(0, len(headerField.values[1].params))
        
    def test_build_header_field_with_methods(self):
        contact = HeaderField()
        contact.name = "Contact"
        hfv = HeaderFieldValue()
        hfv.value = "<sip:test@192.168.1.108>"
        hfv.params["expires"] = "3600"
        contact.values.append(hfv)
        self.assertEqual(contact.write(), "Contact: <sip:test@192.168.1.108>;expires=3600")
        
        