from datetime import datetime

from django.template import RequestContext, loader, Context
from django.http import HttpResponse, Http404

from ideal.security import create_fingerprint, sign_message, posthttps, \
    get_certificate_name, verify_message
from ideal.account import PRIVATE_CERT, MERCHANT_ID, SUB_ID, PRIVATE_KEY, \
    PRIVATE_KEY_PASS, AUTHENTICATION_TYPE, ACQUIRER_HOST, ACQUIRER_PORT, \
    ACQUIRER_PATH, XML_NAMESPACE, CERTIFICATES, CURRENCY, LANGUAGE, \
    ENTRANCE_CODE, EXPIRATION_PERIOD
from ideal.utils import strip_all 
from ideal import parser
    
request_params = (PRIVATE_CERT, PRIVATE_KEY, PRIVATE_KEY_PASS, ACQUIRER_HOST,
    ACQUIRER_PORT, ACQUIRER_PATH)
    
def create_timestamp():
    now = datetime.utcnow()
    timestamp = now.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    return timestamp

def directory_request():
    token = create_fingerprint(PRIVATE_CERT)
    timestamp = create_timestamp()
    message = "".join([timestamp, MERCHANT_ID, SUB_ID])
    token_code = sign_message(PRIVATE_KEY, PRIVATE_KEY_PASS, strip_all(message))
    template = loader.get_template('ideal/dir_req.xml')
    context = Context({
        'timestamp': timestamp,
        'merchant_id': MERCHANT_ID,
        'sub_id': SUB_ID,
        'authentication_type': AUTHENTICATION_TYPE,
        'token': token,
        'token_code': token_code
    })
    request_xml = template.render(context)
    response = posthttps(request_xml, *request_params)
    result = parser.parse_response(response, XML_NAMESPACE)
    return result

def transaction_request(req_data):
    token = create_fingerprint(PRIVATE_CERT)
    timestamp = create_timestamp()
    message = "".join([timestamp, req_data['issuer_id'], MERCHANT_ID, SUB_ID,
        req_data['return_url'], req_data['purchase_id'], req_data['amount'],
        CURRENCY, LANGUAGE, req_data['description'], ENTRANCE_CODE])
    token_code = sign_message(PRIVATE_KEY, PRIVATE_KEY_PASS, strip_all(message))
    template = loader.get_template('ideal/trans_req.xml')
    context = Context({
        'timestamp': timestamp,
        'issuer_id': req_data['issuer_id'],
        'merchant_id': MERCHANT_ID,
        'sub_id': SUB_ID,
        'authentication_type': AUTHENTICATION_TYPE,
        'token': token,
        'token_code': token_code,
        'return_url': req_data['return_url'],
        'purchase_id': req_data['purchase_id'],
        'amount': req_data['amount'],
        'currency': CURRENCY,
        'language': LANGUAGE,
        'description': req_data['description'],
        'entrance_code': ENTRANCE_CODE,
        'expiration_period': EXPIRATION_PERIOD
    })
    request_xml = template.render(context)
    response = posthttps(request_xml, *request_params)
    result = parser.parse_response(response, XML_NAMESPACE)
    return result

def status_request(transaction_id):
    token = create_fingerprint(PRIVATE_CERT)
    timestamp = create_timestamp()
    message = "".join([timestamp, MERCHANT_ID, SUB_ID, transaction_id])
    token_code = sign_message(PRIVATE_KEY, PRIVATE_KEY_PASS, strip_all(message))
    template = loader.get_template('ideal/status_req.xml')
    context = Context({
        'timestamp': timestamp,
        'merchant_id': MERCHANT_ID,
        'sub_id': SUB_ID,
        'authentication_type': AUTHENTICATION_TYPE,
        'token': token,
        'token_code': token_code,
        'transaction_id': transaction_id
    })
    status_request = template.render(context)
    response = posthttps(status_request, *request_params)
    status = parser.parse_response(response, XML_NAMESPACE)
    if status.get('errorCode'):
        return status
    # verify message
    certificate = get_certificate_name(status['fingerprint'], CERTIFICATES)
    if certificate:
        if verify_message(certificate, 
          strip_all("".join([status['createDateTimeStamp'], status['transactionID'], status['status'], status['consumerAccountNumber']])), 
          status['signatureValue']):
            return status
    return False
    