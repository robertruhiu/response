from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from projects.forms import FrameworkForm
from projects.models import Project, Framework
from transactions.models import Transaction, Candidate,OpenCall
from transactions.forms import CandidateForm, SourcingForm
from invitations.models import Invitation
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.core.mail import send_mail, BadHeaderError
# payments view
from payments.views import process_payment


# Create your views here.
def transaction_view(request, id):
    if request.method == 'POST':
        framework_form = FrameworkForm(request.POST)
        if framework_form.is_valid():
            name = framework_form.cleaned_data['name']
            project = Project.objects.get(id=id)
            user = request.user
            new_transaction = Transaction.objects.create(user=user, project=project, stage='upload-candidates', framework=get_object_or_404(Framework, name=name))
            return redirect(reverse('transactions:process_transaction', args=[new_transaction.id]))


def process_transaction(request, id):
    current_transaction = Transaction.objects.get(id=id)
    if current_transaction.stage == 'upload-candidates':
        return upload_candidates(request, current_transaction)
    elif current_transaction.stage == 'payment-stage':
        return all_candidates(request, current_transaction)
    elif current_transaction.stage == 'make-payment':
        return all_candidates(request, current_transaction)
    elif current_transaction.stage == 'payment-confirmed':
        return invitations(request, current_transaction)
    elif current_transaction.stage == 'payment-verified':
        return invitations(request, current_transaction)
    elif current_transaction.stage == 'complete':
        return redirect(reverse('frontend:index'))


def upload_candidates(request, current_transaction):
    # id is transaction id
    mule = current_transaction.id
    # TODO: add capapility to upload text document or csv file of Candidates
    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST)
        if request.POST.get('and_continue'):
            if candidate_form.is_valid():
                current_transaction.stage = 'payment-stage'
                first_name = candidate_form.cleaned_data['first_name']
                last_name = candidate_form.cleaned_data['last_name']
                email = candidate_form.cleaned_data['email']
                new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, email=email,
                                                         transaction=current_transaction)
                new_candidate.save()
                current_transaction.save()
                return redirect(reverse('transactions:process_transaction', args=[current_transaction.id]))

        elif request.POST.get("add_another"):
            if candidate_form.is_valid():
                current_transaction.stage = 'upload-candidates'
                first_name = candidate_form.cleaned_data['first_name']
                last_name = candidate_form.cleaned_data['last_name']
                email = candidate_form.cleaned_data['email']
                new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, email=email,
                                                         transaction=current_transaction)
                new_candidate.save()
                return redirect(reverse('transactions:process_transaction', args=[current_transaction.id]))
        else:
            candidate_form = CandidateForm()
            return render(request, 'transactions/upload_candidate.html', {'candidate_form': candidate_form, 'current_transaction':current_transaction})

    else:
        candidate_form = CandidateForm()
        return render(request, 'transactions/upload_candidate.html', {'candidate_form': candidate_form, 'current_transaction': current_transaction,'mule':mule})


def all_candidates(request, current_transaction):
    #candidates = current_transaction.allcandidates()
    candidates = Candidate.objects.filter(transaction=current_transaction)
    total_amount = current_transaction.amount()
    return render(request, 'transactions/all_candidates.html',
                  {'candidates': candidates,'total_amount': total_amount,
                   'current_transaction': current_transaction})


def invitations(request, current_transaction):
    candidates = Candidate.objects.filter(transaction=current_transaction)
    if request.method == 'POST':
        if candidates.count() != 0:
            for candidate in candidates:
                if User.objects.filter(email=candidate.email).exists():
                    existinguser = User.objects.get(email=candidate.email)
                    send_mail(
                        'Test invitation',
                        'Hello' + ' '+ existinguser.first_name + ' ' + existinguser.last_name + ' ' + 'you have been invited by a Recruiter to partake in a test. '
                        'Use this link to login and access the test invite under Invites: http://beta.codeln.com/accounts/login/',
                        'codeln@codeln.com',
                        [existinguser.email],
                        fail_silently=False,
                    )
                else:             
                    invite = Invitation.create(candidate.email, inviter=request.user)
                    invite.send_invitation(request)

                current_transaction.stage = 'complete'
                current_transaction.save()
        elif candidates.count() == 0:
            current_transaction.stage = 'complete'
            current_transaction.save()
        return redirect(reverse('transactions:process_transaction', args=[current_transaction.id]))
    return render(request, 'transactions/invitations.html',
                  {'candidates': candidates, 'current_transaction': current_transaction})




def my_invites(request):
    candidates = Candidate.objects.filter(email=request.user.email)
    return  render(request, 'transactions/send_credentials.html', {'candidates': candidates})
def success(request):

    return  render(request, 'transactions/success.html')

@login_required
def sourcing(request):
    if request.method == 'POST':
        sourcing_form = SourcingForm(request.POST)
        if sourcing_form.is_valid():
            user = request.user
            subject = 'Sourcing Request'
            from_email = 'codeln@codeln.com'
            jobrole = str(sourcing_form.cleaned_data['job_role'])
            contract = str(sourcing_form.cleaned_data['contract'])
            techstack = sourcing_form.cleaned_data['tech_stack']
            devsneeded = str(sourcing_form.cleaned_data['number_of_devs_needed'])
            pay = str(sourcing_form.cleaned_data['renumeration_in_dollars'])
            html_message = render_to_string('invitations/email/sourcing.html', {'jobrole': jobrole,'contract':contract,'techstack':techstack
                                                                                ,'devsneeded':devsneeded,'pay':pay,'user':user})
            plain_message = strip_tags(html_message)
            from_email = 'codeln@codeln.com'

            try:
                mail.send_mail(subject, plain_message, from_email, ['elohor@codeln.com'], html_message=html_message)
            except BadHeaderError:
                print('invalid error')
            return redirect(reverse('transactions:success'))
    elif request.user.profile.user_type == 'recruiter':
        sourcing_form = SourcingForm()
        return render(request, 'transactions/sourcing.html', {'sourcing_form':sourcing_form})
    else:
        return render(request, 'frontend/landing.html')
def opencall(request,id):
    transaction = Transaction.objects.get(id=id)
    newopencall =OpenCall(recruiter=request.user,project=transaction.project,transaction=transaction)
    newopencall.save()
    transaction.stage = 'make-payment'
    transaction.save()
    amount = 200
    return redirect('transactions:process_transaction' ,transaction.id)

