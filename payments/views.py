from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from transactions.models import Transaction


# Create your views here.

def process_payment(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.stage = 'make-payment'
    amount=int(transaction.amount())
    print(transaction.allcandidates().count())
    transaction.save()
    return render(request, 'payments/process.html',
                  {'amount':amount, 'transaction':transaction})
def process_opencalloption1(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.stage = 'make-payment'
    amount= int(400)
    print(transaction.allcandidates().count())
    transaction.save()
    return render(request, 'payments/process.html',
                  {'amount':amount, 'transaction':transaction})

def process_opencalloption2(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.stage = 'make-payment'
    amount=int(600)
    print(transaction.allcandidates().count())
    transaction.save()
    return render(request, 'payments/process.html',
                  {'amount':amount, 'transaction':transaction})

def process_opencalloption3(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.stage = 'make-payment'
    amount=int(800)
    print(transaction.allcandidates().count())
    transaction.save()
    return render(request, 'payments/process.html',
                  {'amount':amount, 'transaction':transaction})
@csrf_exempt
def payment_canceled(request, id):
    # redirect to add candidates
    return redirect(reverse('transactions:process_transaction', args=[id]))


@csrf_exempt
def flutterwavepayment_done(request, id):
    transaction = Transaction.objects.get(id=id)
    transaction.stage = 'payment-verified'
    transaction.paid = True
    transaction.save()
    # verifypaymentsuccess
    return redirect(reverse('transactions:process_transaction', args=[transaction.id]))
