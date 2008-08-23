from django.db import models

class Transaction(models.Model):
    """iDEAL transaction"""
    purchase_id = models.AutoField('purchase id', primary_key=True)
    order_id = models.CharField(blank=True, null=True, max_length=20)
    amount = models.IntegerField(blank=True, null=True)
    issuer_id = models.CharField(blank=True, max_length=4)
    status = models.CharField(blank=True, max_length=10)
    transaction_id = models.CharField(blank=True, max_length=16)
    consumer_name = models.CharField(blank=True, null=True, max_length=35)
    consumer_account_numer = models.CharField(blank=True, null=True, max_length=10)
    consumer_city = models.CharField(blank=True, null=True, max_length=24)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    expires = models.DateTimeField(blank=True, null=True)
    
class Traffic(models.Model):
    """HTTP traffic"""
    request  = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
