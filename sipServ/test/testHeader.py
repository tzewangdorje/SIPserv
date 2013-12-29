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
        # more complex
        line = "Via: SIP/2.0/UDP 127.0.0.1;branch=z9hG4bKufswnhxy;rport"
        headerField = HeaderField(line)
        self.assertEqual(line, headerField.write())
        # multiple values
        line = "Allow: INVITE,ACK,BYE,CANCEL,OPTIONS,PRACK,REFER,NOTIFY,SUBSCRIBE,INFO,MESSAGE"
        headerField = HeaderField(line)
        self.assertEqual(line, headerField.write())
        self.assertEqual(11, len(headerField.values))
        self.assertEqual("INVITE", str(headerField.values[0]))
        self.assertEqual("HeaderFieldValue", type(headerField.values[0]).__name__)
        
        