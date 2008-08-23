import os

from ideal import security, parser
from ideal.account import XML_NAMESPACE
from ideal.checkout import directory_request

from django.test import TestCase

MODULE_HOME = os.path.dirname(os.path.abspath(__file__))

class SecurityTest(TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_fingerprint(self):
        cert_path = os.path.join(MODULE_HOME, "merchantprivatecert.cer")
        fingerprint = security.create_fingerprint(cert_path)
        self.assertEqual("2A2D7E883458655985354EA727CDF6681DD7DD9C", fingerprint)
    
    def test_sign_message(self):
        self.assertEqual("Uag3Ycrn/B9gaTFwRXs7eYIl8f7one79Ur66UhSEaCpleopQvouZlecCZTuFIBqAaR08UnaxvmKiE/5bAaMz1koblE1nbmtmY5GmOM898nTF+/qySORJUiUed/gjbHupGq0b5R5KXqAn3wDBELgytoKEW9bBdHdORpF8U589nog=", 
            security.sign_message(os.path.join(MODULE_HOME, "merchantprivatekey.pem"), 
            'test', "2006-05-10T14:06:20.000Z0050342310"))
    
    def test_verify_message(self):
        self.assertEqual(True,
            security.verify_message(os.path.join(MODULE_HOME, "ideal.cer"), 
            "2006-05-10T14:06:52.287Z0050000005922889SuccessP012345678", 
            "rlqtzbL5qiIEh4GJB5JmKAOz6aDSY+1NL3y5qigmHj9Fuveyoni5RY78v/tuC76boOqzLuXv6PMA1CYiK1iE7ATfY+/7UlFdc/Qp5qa2ZLjEWa8dAf9e/4KjYmPTNnSdB6VCky0iBUzi54qXwSmqWcuwQE/5pQfod0qYPR2I+8E=")
        )
    
    def test_get_certificate_name(self):
        cert_name = "ideal.cer"
        cert_path = os.path.join(MODULE_HOME, cert_name)
        self.assertEqual(cert_path,
            security.get_certificate_name("03A07E0584AF7F715CEBD3702477555C52F11AEF", (cert_path, ))
        )
        
class ParserTest(TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_parse_dir_res(self):
        fd = open(os.path.join(MODULE_HOME, "dir_res.xml"), "rb")
        resp = fd.read()
        fd.close()
        result = parser.parse_response(resp, namespace=XML_NAMESPACE)
        expected = {'acquirerID': '0050', 'issuers': [{'issuerID': '0151', 
            'issuerList': 'Short', 'issuerName': 'Issuer Simulator'}]}
        self.assertEqual(expected, result)
        
    def test_parse_trans_res(self):
        fd = open(os.path.join(MODULE_HOME, "trans_res.xml"), "rb")
        resp = fd.read()
        fd.close()
        result = parser.parse_response(resp, namespace=XML_NAMESPACE)
        expected = {'purchaseID': '9459897270157938', 
            'transactionID': '1726846372615234', 
            'issuerAuthenticationURL': 'https://idealtest.rabobank.nl/ideal/issuerSim.do?trxid=1726846372615234&ideal=prob', 
            'acquirerID': '0050'}
        self.assertEqual(expected, result)
        
    def test_parse_status_res(self):
        fd = open(os.path.join(MODULE_HOME, "status_res.xml"), "rb")
        resp = fd.read()
        fd.close()
        result = parser.parse_response(resp, namespace=XML_NAMESPACE)
        expected = {'status': 'Success', 'consumerName': None, 
            'createDateTimeStamp': '2000-12-28T13:59:59.393Z', 
            'fingerprint': None, 'transactionID': '1726846372615234', 
            'consumerAccountNumber': None, 'consumerCity': 'DEN HAAG', 
            'signatureValue': None}
        self.assertEqual(expected, result)
        
    def test_parse_error_res(self):
        fd = open(os.path.join(MODULE_HOME, "error_res.1.xml"), "rb")
        resp = fd.read()
        fd.close()
        result = parser.parse_response(resp, namespace=XML_NAMESPACE)
        expected = {'createDateTimeStamp': '2000-12-28T13:59:59.393Z', 
            'errorCode': 'SE2700', 'errorMessage': 'Invalid electronic signature',
            'errorDetail': None, 'suggestedAction': None, 
            'suggestedExpirationPeriod': None, 'consumerMessage': 'Invalid electronic signature'}
        self.assertEqual(expected, result)
        
class CheckoutTest(TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    def test_directory_request(self):
        directory = directory_request()
        self.assertEqual("0050", directory['acquirerID'])
        self.assertEqual(1, len(directory['issuers']))
        self.assertEqual("Issuer Simulator", directory['issuers'][0]['issuerName'])
        self.assertEqual("0151", directory['issuers'][0]['issuerID'])
        self.assertEqual("Short", directory['issuers'][0]['issuerList'])
        
    # def test_return_errors(self):
    #     raise
    #     
    # def test_transaction_request(self):
    #     raise
    #     
    # def test_transaction_cancel(self):
    #     raise
    #     
    # def test_transaction_expired(self):
    #     raise
    #     
    # def test_transaction_open(self):
    #     raise
    #     
    # def test_transaction_failed(self):
    #     raise
    #     
    # def test_transaction_verify_failed(self):
    #     raise
    #     
    # def test_index(self):
    #     raise
    #     
    # def test_confirm(self):
    #     raise
