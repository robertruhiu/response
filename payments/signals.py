from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from transactions.models import Transaction


def payment_notification(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        transaction = get_object_or_404(Transaction, id=ipn_obj.invoice)
        transaction.stage = 'payment-verified'
        transaction.paid = True
        transaction.save()

valid_ipn_received.connect(payment_notification)
