from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext
from django.views.decorators.http import require_GET
from django.core.mail import mail_admins
from django.shortcuts import get_object_or_404, render_to_response

from ideal.checkout import status_request, directory_request, transaction_request
from ideal.models import Transaction
from ideal.forms import TestPaymentForm
from ideal.account import MERCHANT_RETURN_DOMAIN

def request_transaction(amount, issuer_id, order_id=None):
    trx = Transaction(amount=amount, issuer_id=issuer_id, order_id=order_id)
    trx.status = 'Pending'
    trx.save()
    return_url = '%s%s' % (MERCHANT_RETURN_DOMAIN, reverse('ideal_return_url'))
    req_data = {
        'issuer_id': issuer_id,
        'purchase_id': str(trx.purchase_id),
        'amount': str(amount),
        'description': 'iDEAL payment',
        'return_url': return_url,
    }
    transaction = transaction_request(req_data)
    if transaction and transaction.get('errorCode'):
        trx.status = 'Error'
        trx.save()
        return False
    try:
        trx = Transaction.objects.get(purchase_id=transaction['purchaseID'])
    except Exception, info:
        mail_admins("iDEAL: error message (request_transaction)", 
            "error fetching Transaction object: %s" % info, fail_silently=True)
        return False
    else:
        trx.transaction_id = transaction['transactionID']
        trx.status = 'Requested'
        trx.save()
    return transaction

@require_GET
def status(request):
    try:
        transaction_id = request.GET['trxid']
    except KeyError:
        return HttpResponse("error: wrong url")
    status = status_request(transaction_id)
    if status and status.get('status') == 'Success':
        # update ideal transaction
        trx = get_object_or_404(Transaction, transaction_id=transaction_id)
        trx.status = status.get('status')
        trx.save()
        # NB: dispatch/send a post-payed signal here to notify listeners?
        return HttpResponse("You have payed!!!")
    elif status and status.get('status'):
        trx = get_object_or_404(Transaction, transaction_id=transaction_id)
        trx.status = status.get('status')
        trx.save()
        return HttpResponse("payment status: %s" % status.get('status'))
    else:
        # show error page
        return HttpResponse("error: unknown status")

def test_form(request):
    if request.method == 'POST':
        form = TestPaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            issuer_id = form.cleaned_data['issuer_id']
            transaction = request_transaction(amount, issuer_id)
            if transaction and transaction.get('issuerAuthenticationURL'):
                redirect_to = transaction['issuerAuthenticationURL']
                return HttpResponseRedirect(redirect_to)
            else:
                return HttpResponse("dev: an error occurred; see ideal_traffic"\
                    " table for details")
    else:
        form = TestPaymentForm()
    return render_to_response('ideal/test_payment.html', {'form': form})
    
    
            
