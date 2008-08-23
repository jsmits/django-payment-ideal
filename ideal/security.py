"Methods for creating security tokens."
import base64
import hashlib

import os
import M2Crypto
import socket
import ssl # new python ssl module
import httplib
import os.path

from ideal.models import Traffic

class HTTPSConnection(httplib.HTTPSConnection):
    """An HTTPS connection using the ssl module
    
    An HTTPS connection implementation that does not:

        * depend on swig
        * ignore server certificates

    $Id: __init__.py 81831 2007-11-14 13:19:41Z alga $
    
    Based on zc.ssl's HTTPSConnection.
    
    See http://xivilization.net/pydocs/2.6/library/ssl.html for module docs.
    """

    def __init__(self, host, port=None, key_file=None, cert_file=None,
                 strict=None, timeout=None):
        # timeout is None or float
        self.timeout = timeout
        httplib.HTTPSConnection.__init__(self, host, port, key_file, cert_file,
                                         strict)
        if self.cert_file is None:
            self.cert_file = os.path.join(os.path.dirname(__file__),
                                          "certs.pem")

    ssl_wrap_socket = staticmethod(ssl.wrap_socket)

    def connect(self):
        "Connect to a host on a given (SSL) port."
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = self.ssl_wrap_socket(sock)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

def create_fingerprint(cert_file):
    cert = M2Crypto.X509.load_cert(cert_file)
    cert_data = cert.as_pem()
    cert_data = cert_data.replace("-----BEGIN CERTIFICATE-----", "")
    cert_data = cert_data.replace("-----END CERTIFICATE-----", "")
    fingerprint = base64.b64decode(cert_data)
    sha = hashlib.sha1() # this must be hashlib's sha1, because the fingerprint needs to be hex digested
    sha.update(fingerprint)
    fingerprint = sha.hexdigest()
    return fingerprint.upper()
    
def sign_message(privatekey_file, passphrase, message):
    def passphrase_callback(passphrase):
        def inner(v): return passphrase
        return inner
    private_key = M2Crypto.RSA.load_key(privatekey_file, 
        callback=passphrase_callback(passphrase))
    sha1 = M2Crypto.EVP.MessageDigest('sha1')
    sha1.update(message)
    digest = sha1.digest()
    sign = private_key.sign(digest)
    signature = base64.b64encode(sign).replace("\n", "")
    return signature
    
def verify_message(cert_file, message, signature):
    cert = M2Crypto.X509.load_cert(cert_file)
    pub_key = cert.get_pubkey()
    pub_key.verify_init()
    pub_key.verify_update(message)
    sign = base64.b64decode(signature)
    return pub_key.verify_final(sign)
    
def posthttps(data, cert_file, key_file, key_pass, host, port, path):
    conn = HTTPSConnection(host, port, key_file, cert_file)
    # conn.set_debuglevel(5)
    conn.request("POST", path, data)
    response = conn.getresponse()
    body = response.read()
    traffic = Traffic(request=data, response=body)
    traffic.save()
    return body
    
def get_certificate_name(fingerprint, certifcate_paths):
    for cert_path in certifcate_paths:
        if fingerprint == create_fingerprint(cert_path):
            return cert_path
            