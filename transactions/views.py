from django.shortcuts import render, redirect
from django.urls import reverse

from projects.models import Project
from transactions.models import Transaction, Candidate
from transactions.forms import CandidateForm


# Create your views here.
def transaction(request, id):
    project = Project.objects.get(id=id)
    user = request.user
    new_transaction = Transaction.objects.get_or_create(user=user, project=project, stage='payment')
    return redirect(reverse('transactions:upload-candidates', args=new_transaction))



def upload_candidates(request):
    # id is transaction id
    # TODO: add capapility to upload text document or csv file of Candidates
    if request.method == 'POST':
        candidate_form = CandidateForm(request.POST)
        if request.POST.get('and_continue'):
            if candidate_form.is_valid():
                first_name = candidate_form.cleaned_data['first_name']
                last_name = candidate_form.cleaned_data['last_name']
                email = candidate_form.cleaned_data['email']
                transaction = new
                new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, email=email,
                                                         transaction=transaction)
                new_candidate.save()
                return redirect(reverse('transactions:all-candidates',))

        elif request.POST.get("add_another"):
            if candidate_form.is_valid():
                first_name = candidate_form.cleaned_data['first_name']
                last_name = candidate_form.cleaned_data['last_name']
                email = candidate_form.cleaned_data['email']
                transaction = trans
                new_candidate = Candidate.objects.create(first_name=first_name, last_name=last_name, email=email,
                                                         transaction=transaction)
                new_candidate.save()
                return redirect(reverse('transactions:transaction', args=(project,)))
        else:
            candidate_form = CandidateForm()
            return render(request, 'transactions/upload_candidate.html', {'candidate_form': candidate_form})

    else:
        candidate_form = CandidateForm()
        return render(request, 'transactions/upload_candidate.html', {'candidate_form': candidate_form})

def all_candidates(request):
    pass
