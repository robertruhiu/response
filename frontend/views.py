from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# Create your views here.
from django.urls import reverse

from accounts.forms import ProfileTypeForm, DeveloperFillingDetailsForm, RecruiterFillingDetailsForm
from transactions.models import Transaction , Candidate
from invitations.models import Invitation
from projects.models import Project
from frontend.form import Projectinvite
from frontend.models import candidatesprojects,devs,recruiters


@login_required
def developer_filling_details(request, current_profile):
    if request.method == 'POST':
        developer_filling_details_form = DeveloperFillingDetailsForm(request.POST, request.FILES)
        if developer_filling_details_form.is_valid():

            current_profile.github_repo = developer_filling_details_form.cleaned_data['github_repo']
            current_profile.linkedin_url = developer_filling_details_form.cleaned_data['linkedin_url']
            current_profile.portfolio = developer_filling_details_form.cleaned_data['portfolio']
            current_profile.language = developer_filling_details_form.cleaned_data['language']
            current_profile.framework = developer_filling_details_form.cleaned_data['framework']
            current_profile.years = developer_filling_details_form.cleaned_data['years'],
            current_profile.gender = developer_filling_details_form.cleaned_data['gender']
            current_profile.availabilty = developer_filling_details_form.cleaned_data['availabilty']
            current_profile.country = developer_filling_details_form.cleaned_data['country']
            current_profile.phone_number = developer_filling_details_form.cleaned_data['phone_number']
            current_profile.stage = 'complete'
            current_profile.save()
            return redirect(reverse('frontend:index'))
    else:
        developer_filling_details_form = DeveloperFillingDetailsForm()
    return render(request, 'frontend/developer/developer_filling_details.html',
                  {'developer_filling_details_form': developer_filling_details_form})

@login_required
def recruiter_filling_details(request, current_profile):
    if request.method == 'POST':
        recruiter_filling_details_form = RecruiterFillingDetailsForm(request.POST)
        if recruiter_filling_details_form.is_valid():
            current_profile.company = recruiter_filling_details_form.cleaned_data['company']
            current_profile.job_role = recruiter_filling_details_form.cleaned_data['job_role']
            current_profile.industry = recruiter_filling_details_form.cleaned_data['industry']
            current_profile.country = recruiter_filling_details_form.cleaned_data['country']
            current_profile.company_url = recruiter_filling_details_form.cleaned_data['company_url']
            current_profile.stage = 'complete'
            current_profile.save()
            return redirect(reverse('frontend:index'))
    else:
        recruiter_filling_details_form = RecruiterFillingDetailsForm()
    return render(request, 'frontend/recruiter/recruiter_filling_details.html',
                  {'recruiter_filling_details_form': recruiter_filling_details_form})

@login_required
def profile_type_selection(request, current_profile):
    if request.method == 'POST':
        profile_type_form = ProfileTypeForm(request.POST)
        if profile_type_form.is_valid():
            profile_type = profile_type_form.cleaned_data['profile_type']
            current_profile.user_type = profile_type
            if profile_type == 'developer':
                current_profile.stage = 'developer_filling_details'
                # test_registration = Student(user=request.user)
                # test_registration.save()
            elif profile_type == 'recruiter':
                current_profile.stage = 'recruiter_filling_details'
            current_profile.save()
            return redirect(reverse('frontend:index'))
    else:
        profile_type_form = ProfileTypeForm()
    return render(request, 'frontend/profile_type_selection.html', {'profile_type_form': profile_type_form})


def index(request):
    if request.user.is_authenticated:
        current_profile = request.user.profile
        transactions = Transaction.objects.filter(user=request.user)
        if request.user.profile.stage == 'profile_type_selection':
            return profile_type_selection(request, current_profile)
        elif request.user.profile.stage == 'developer_filling_details':
            return developer_filling_details(request, current_profile)
        elif request.user.profile.stage == 'recruiter_filling_details':
            return recruiter_filling_details(request, current_profile)
        elif request.user.profile.stage == 'complete':
            if request.user.profile.user_type == 'developer':
                return render(request, 'frontend/developer/developer.html')
            elif request.user.profile.user_type == 'recruiter':
                return render(request, 'frontend/recruiter/recruiter.html', {'transactions': transactions})
    else:
        return home(request)


def home(request):
    return render(request, 'frontend/landing.html')


@login_required
def activity(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user)
        if request.user.profile.user_type == 'recruiter':
            return render(request, 'frontend/recruiter/my-activity.html', {'transactions': transactions})
        elif request.user.profile.user_type == 'developer':
            return render(request, 'frontend/developer/my-activity.html', {'transactions': transactions})


def tracker(request, id):
    project =Transaction.objects.get(id = id)
    candidates = candidatesprojects.objects.filter(transaction=id)


    return render(request, 'frontend/recruiter/tracker.html', {'candidates': candidates,'project':project})


@login_required
def inprogress(request, user_id):
    projects=candidatesprojects.objects.filter(candidate=user_id)
    return render(request, 'frontend/developer/inprogress.html',{'projects':projects})

@login_required
def invites(request):
    candidates = Candidate.objects.filter(email=request.user.email)
    return render(request, 'frontend/developer/invites.html', {'candidates': candidates})


@login_required
def projectdetails(request, id):
    projectinvite=Projectinvite()
    project =candidatesprojects.objects.get(id=id)
    return render(request, 'frontend/developer/projectdetails.html', {'project': project,'projectinvite':projectinvite})


@login_required
def pendingproject(request,  transaction_id):
        acceptedinvites=candidatesprojects.objects.filter(transaction_id=transaction_id,candidate=request.user)
        transaction = Transaction.objects.get(id=transaction_id)

        return render(request, 'frontend/developer/pendingproject.html',
                      { 'transaction': transaction,'acceptedinvites':acceptedinvites})


def projectinvites(request,transaction_id,candidate_id):
    trans_id =Transaction.objects.get(id=transaction_id)
    currentcandidate =User.objects.get(id=candidate_id)

    acceptedinvite = candidatesprojects(transaction=trans_id, candidate=currentcandidate,stage='invite-accepted')
    acceptedinvite.save()
    return render(request, 'frontend/developer/developer.html')

def update_candidateprojects(request,candidateproject_id,transaction_id):
        transaction =Transaction.objects.get(id=transaction_id)
        candidatesproject =candidatesprojects.objects.get(id=candidateproject_id)
        candidatesproject.stage ='project-in-progress'
        candidatesproject.save()
        return HttpResponseRedirect('/projectdetails/%s' % candidateproject_id)

def update_finished(request,candidateproject_id,transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    candidatesproject = candidatesprojects.objects.get(id=candidateproject_id)
    candidatesproject.stage = 'project-completed'
    candidatesproject.save()
    return HttpResponseRedirect('/projectdetails/%s' % candidateproject_id)


def pricing(request):
    return render(request, 'frontend/pricing.html')


def dev(request):
    return render(request, 'frontend/dev.html')


def howitworks(request):
    return render(request, 'frontend/how.html')


def report(request, email, transaction_id):
    user = User.objects.get(email=email)
    transaction = Transaction.objects.get(id=transaction_id)
    return render(request, 'frontend/recruiter/report.html', {'user': user, 'transaction': transaction})

def onboarddevs(request):
    for alluser in User.objects.all():
        if alluser.profile.user_type == 'developer':
            if alluser.profile.stage == 'complete':
                if not devs.objects.filter(email=alluser.email).exists():
                    dev = devs()
                    dev.email=alluser.email
                    dev.firstname = alluser.first_name
                    dev.lastname = alluser.last_name
                    dev.language = alluser.profile.language
                    dev.framework = alluser.profile.framework
                    dev.country = alluser.profile.country
                    dev.github =alluser.profile.github_repo
                    dev.linkedin = alluser.profile.linkedin_url
                    dev.portfolio = alluser.profile.portfolio
                    dev.save()

    return redirect(reverse('frontend:seedevs'))

def onboardrecruiters(request):
    for alluser in User.objects.all():
        if alluser.profile.user_type == 'recruiter':
            if alluser.profile.stage == 'complete':
                if not recruiters.objects.filter(email=alluser.email).exists():
                    recruiter = recruiters()
                    recruiter.email=alluser.email
                    recruiter.firstname = alluser.first_name
                    recruiter.lastname = alluser.last_name
                    recruiter.company = alluser.profile.company
                    recruiter.companyurl = alluser.profile.company_url
                    recruiter.country = alluser.profile.country
                    recruiter.save()

    return redirect(reverse('frontend:seerecruiters'))


def credits(request):
    return render(request, 'frontend/credits.html')


def privacy(request):
    return render(request, 'frontend/privacy.html')


def terms(request):
    return render(request, 'frontend/terms.html')


def sample(request):
    return render(request, 'frontend/sample.html')


def page_404(request):
    return render(request, 'frontend/error_pages/404.html')


def page_500(request):
    return render(request, 'frontend/error_pages/500.html')

def seedevs(request):
    developers =devs.objects.all()
    return render(request, 'frontend/recruiter/devlist.html',{'developers':developers})

def seerecruiters(request):
    payers =recruiters.objects.all()
    return render(request, 'frontend/recruiter/recruiterslist.html',{'payers':payers})

def manageprojects(request):
    projects =Project.objects.all()
    return render(request, 'frontend/recruiter/projects.html',{'projects':projects})

def managetransactions(request):
    transactions =Transaction.objects.all()
    return render(request,'frontend/recruiter/transactions.html',{'transactions':transactions})


