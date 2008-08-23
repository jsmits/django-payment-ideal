# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext

ISSUERS = (
    ('0031', 'ABN Amro Bank'),
    ('0721', 'Postbank'),
    ('0021', 'Rabobank'),
    ('0081', 'Fortis'),
    ('0751', 'SNS Bank'),
)

AMOUNT_CHOICES = (
    ('1250', "12,50"), 
    ('2500', "25,00"), 
    ('5000', "50,00"), 
    ('7500', "75,00"),
)

class TestPaymentForm(forms.Form):
    issuer_id = forms.ChoiceField(label=ugettext('bank'), choices=ISSUERS)
    amount = forms.ChoiceField(label=ugettext('amount'), choices=AMOUNT_CHOICES) 
    
