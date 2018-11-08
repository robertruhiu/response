from django.shortcuts import render, redirect
from django.urls import reverse

from projects.models import Project
from transactions.models import Transaction, Candidate
from transactions.forms import CandidateForm, SourcingForm
from invitations.models import Invitation


from django.core.mail import send_mail, BadHeaderError
# payments view
from payments.views import process_payment


# Create your views here.
def transaction(request, id):
    project = Project.objects.get(id=id)
    user = request.user
    new_transaction = Transaction.objects.create(user=user, project=project, stage='upload-candidates')
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
        return render(request, 'transactions/upload_candidate.html', {'candidate_form': candidate_form, 'current_transaction': current_transaction})


def all_candidates(request, current_transaction):
    # candidates = current_transaction.allcandidates()
    candidates = Candidate.objects.filter(transaction=current_transaction)
    count = candidates.count()
    total_amount = count * 20
    return render(request, 'transactions/all_candidates.html',
                  {'candidates': candidates, 'count': count, 'total_amount': total_amount,
                   'current_transaction': current_transaction})


def invitations(request, current_transaction):
    candidates = Candidate.objects.filter(transaction=current_transaction)
    if request.method == 'POST':
        if candidates.count() != 0:
            for candidate in candidates:
                invite = Invitation.create(candidate.email, inviter=request.user)
                invite.send_invitation(request)
            current_transaction.stage = 'complete'
            current_transaction.save()
        return redirect(reverse('transactions:process_transaction', args=[current_transaction.id]))
    return render(request, 'transactions/invitations.html',
                  {'candidates': candidates, 'current_transaction': current_transaction})



def my_invites(request):
    candidates = Candidate.objects.filter(email=request.user.email)
    return  render(request, 'transactions/send_credentials.html', {'candidates': candidates})


def sourcing(request):
    if request.method == 'POST':
        form = SourcingForm(request.POST)
        if form.is_valid():
            subject = 'Sourcing Request'
            from_email = form.cleaned_data['email_address']
            data = ""
            data += form.cleaned_data['name']
            data += str(form.cleaned_data['phone_number'])
            data += form.cleaned_data['company_name']
            data += str(form.cleaned_data['job_role'])
            data += form.cleaned_data['engagement_types']
            data += form.cleaned_data['tech_stack']
            data += form.cleaned_data['project_description']
            data += str(form.cleaned_data['devs_needed'])
            data += str(form.cleaned_data['renumeration'])
            data += form.cleaned_data['tech_staff']
            data += form.cleaned_data['skills_test']
            try:
                send_mail(subject, data, from_email, ['philisiah@codeln.com'])
            except BadHeaderError:
                print('invalid error')
            return redirect('frontend:home')
    else:
        form = SourcingForm()
        return render(request, 'transactions/sourcing.html', {'form':form})
