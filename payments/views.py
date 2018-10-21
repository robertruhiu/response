from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from transactions.models import Transaction


# Create your views here.

def process_payment(request, id, amount):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.stage = 'make-payment'
    transaction.save()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': transaction.amount(),
        'item_name': transaction.user,
        'invoice': str(transaction.project.id),
        'currency_code': 'USD',
        'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),
        'return_url': request.build_absolute_uri(reverse('payments:done', args=[transaction.id])),
        'cancel_return': request.build_absolute_uri(reverse('payments:canceled', args=[transaction.id])),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payments/process.html',
                  {'form': form, 'transaction': transaction, 'amount':amount})

@csrf_exempt
def payment_done(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.stage = 'payment-confirmed'
    transaction.save()
    #verifypaymentsuccess
    return redirect(reverse('transactions:process_transaction', args=[transaction.id]))


@csrf_exempt
def payment_canceled(request, id):
    #redirect to add candidates
    return  redirect(reverse('transactions:process_transaction', args=[id]))
