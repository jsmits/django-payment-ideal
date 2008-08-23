try:
    import xml.etree.ElementTree as ET # in python >= 2.5
except ImportError:
    try:
        import cElementTree as ET # effbot's C module
    except ImportError:
        try:
            import elementtree.ElementTree as ET # effbot's pure Python module
        except ImportError:
            try:
                import lxml.etree as ET # ElementTree API using libxml2
            except ImportError:
                raise ImportError("ElementTree was not found. iDEAL app" \
                    " requires ElementTree.")

from django.core.mail import mail_admins

def handle_response(type, body):
    if type == "ErrorRes" or type == "unknown":
        mail_admins("iDEAL: %s message" % type, body, fail_silently=True)
    
def parse_response(xml, namespace=None):
    tree = ET.fromstring(xml)
    parsers = {
        "DirectoryRes": parse_dir_res,
        "AcquirerTrxRes": parse_trans_res,
        "AcquirerStatusRes": parse_status_res,
        "ErrorRes": parse_error_res,
    }
    for message_type, parser in parsers.items():
        tag_name = full_qname_text((message_type, ), namespace)
        if tree.tag == tag_name:
            handle_response(message_type, xml)
            return parser(tree, namespace)
    handle_response("unknown", xml)
    raise Exception("unknown message")
    
def element_qname(tag, namespace=None):
    if namespace:
        return ET.QName(namespace, tag)
    else:
        return ET.QName(tag)
    
def full_qname_text(tag_tuple, namespace=None):
    nodes = []
    for tag in tag_tuple:
        qname = element_qname(tag, namespace)
        nodes.append(qname.text)
    full_qname_text = "/".join(nodes)
    return full_qname_text
    
def local_name(tag_name, namespace):
    name = tag_name.replace('{%s}' % namespace, '')
    return name
    
def parse_dir_res(tree, namespace=None):
    result = {}
    issuerlist = []
    element_name = full_qname_text(("Directory", "Issuer"), namespace)
    for issuer_tag in tree.findall(element_name):
        issuer = {}
        for element in issuer_tag:
            issuer[local_name(element.tag, namespace)] = element.text
        issuerlist.append(issuer)
    result.update({'issuers': issuerlist})
    element_name = full_qname_text(("Acquirer", "acquirerID"), namespace)
    acquirer_id = tree.find(element_name)
    result.update({local_name(acquirer_id.tag, namespace): acquirer_id.text})
    return result

def parse_trans_res(tree, namespace=None):
    tags = (
        ("Transaction", "transactionID"), 
        ("Transaction", "purchaseID"),
        ("Acquirer", "acquirerID"), 
        ("Issuer", "issuerAuthenticationURL"),
    )
    result = {}
    for tag in tags:
        element_name = full_qname_text(tag, namespace)
        element = tree.find(element_name)
        if element == None:
            raise Exception("Tag %s not found." % str(tag))
        result.update({local_name(element.tag, namespace): element.text})
    return result
    
def parse_status_res(tree, namespace=None):
    tags = (
        ("createDateTimeStamp", ), 
        ("Transaction", "transactionID"), 
        ("Transaction", "status"), 
        ("Signature", "signatureValue"), 
        ("Signature", "fingerprint"),
    )
    optional_tags = (
        ("Transaction", "consumerName"), 
        ("Transaction", "consumerCity"),
        ("Transaction", "consumerAccountNumber"),
    )
    result = {}
    for tag in tags:
        element_name = full_qname_text(tag, namespace)
        element = tree.find(element_name)
        if element == None: 
            raise Exception("Required tag %s not found." % str(tag))
        result.update({local_name(element.tag, namespace): element.text})
    for tag in optional_tags:
        element_name = full_qname_text(tag, namespace)
        element = tree.find(element_name)
        if element != None:
            result.update({local_name(element.tag, namespace): element.text})
    return result
    
def parse_error_res(tree, namespace=None):
    tags = (
        ("createDateTimeStamp", ), 
        ("Error", "errorCode"), 
        ("Error", "errorMessage"),
    )
    optional_tags = (
        ("Error", "errorDetail"), 
        ("Error", "suggestedAction"), 
        ("Error", "suggestedExpirationPeriod"), 
        ("Error", "consumerMessage"),
    )
    result = {}
    for tag in tags:
        element_name = full_qname_text(tag, namespace)
        element = tree.find(element_name)
        if element == None: 
            raise Exception("Required tag %s not found." % str(tag))
        result.update({local_name(element.tag, namespace): element.text})
    for tag in optional_tags:
        element_name = full_qname_text(tag, namespace)
        element = tree.find(element_name)
        if element != None:
            result.update({local_name(element.tag, namespace): element.text})
    return result
    
        