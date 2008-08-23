# Configuration file iDEAL Advanced
# Python implementation
# See documentation for more info
# (c) Sander Smits
import os, sys

MODULE_HOME = os.path.dirname(os.path.abspath(__file__))
def full_path(file_path):
    return os.path.join(MODULE_HOME, file_path)

# This section defines the variables used to create your own RSA private key 
# and the certificate based on this key
# Default values enables you to test the example demoshop
# Do not change AUTHENTICATION_TYPE unless you have specific reasons to do so
PRIVATE_KEY = full_path("certificates/merchantprivatekey.pem")
PRIVATE_KEY_PASS = "test"
PRIVATE_CERT = full_path("certificates/merchantprivatecert.cer")
AUTHENTICATION_TYPE = "SHA1_RSA"

# CERTIFICATES[0] contains the signing certificate of your acquirer
# This field should not be changed
CERTIFICATES = (
    full_path("certificates/ideal.cer"), 
)

# Address of the iDEAL acquiring server
# Use ssl://idealtest.rabobank.nl:443/ideal/iDeal during integration/test
# Use ssl://ideal.rabobank.nl:443/ideal/iDeal only for production
# Do not change ACQUIRER_TIMEOUT unless you have specific reasons to do so
# ACQUIRER_URL = "ssl://ideal.rabobank.nl:443/ideal/iDeal" # production
# ACQUIRER_HOST = "ideal.rabobank.nl" # production
ACQUIRER_URL = "ssl://idealtest.rabobank.nl:443/ideal/mpiPayInitRabo.do" # test
ACQUIRER_HOST = "idealtest.rabobank.nl" # test
ACQUIRER_PATH = "/ideal/iDeal"
ACQUIRER_PORT = 443
ACQUIRER_TIMEOUT = 10

# Default MERCHANT_ID enables you to test the example demoshop
# Your own MERCHANT_ID can be retrieved via the iDEAL Dashboard
# Do not change SUB_ID unless you have specific reasons to do so
MERCHANT_ID = "123456789" 
SUB_ID = "0"

# MERCHANT_RETURN_DOMAIN is the domain on your system that the customer is 
# redirected to after the iDEAL payment. It is used to construct the return url 
# dynamically. The return url should carry out the Status Request.
MERCHANT_RETURN_DOMAIN = "http://localhost:8000"

# Do not change currenty unless you have specific reasons to do so
CURRENCY = "EUR"

# EXPIRATION_PERIOD is the timeframe during which the transaction is allowed to take place
# Maximum is PT1H (1 hour)
EXPIRATION_PERIOD = "PT10M"

# LANGUAGE is only used for showing error messages in the prefered language
# LANGUAGE = "en"
LANGUAGE = "nl"

# Default DESCRIPTION
# Used when you do not want to use transaction specific descriptions
DESCRIPTION = "iDeal betalingstransactie"

# Default ENTRANCE_CODE
# Used when you do not want to use transaction specific entrance codes
# See documentation for more info
ENTRANCE_CODE = "12345678"

XML_NAMESPACE = "http://www.idealdesk.com/Message"
