from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.core.paginator import Paginator
from collections import Counter
from django.urls import reverse
import requests

import json
from decouple import config

import base64
import urllib.parse
from django.contrib import messages
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from accounts.forms import ProfileTypeForm, DeveloperFillingDetailsForm, RecruiterFillingDetailsForm
from transactions.models import Transaction, Candidate,OpenCall,Applications
from invitations.models import Invitation
from projects.models import Project, Framework
from frontend.form import Projectinvite, EditProjectForm,Submissions,Portfolio_form,Github_form,Experience_Form
from frontend.models import candidatesprojects, devs, recruiters,submissions,Portfolio,Github,Experience
from classroom.models import TakenQuiz,Student
from marketplace.models import Job

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
        transactions = Transaction.objects.filter(user=request.user).filter(stage='complete')
        if request.user.profile.stage == 'profile_type_selection':
            return profile_type_selection(request, current_profile)
        elif request.user.profile.stage == 'developer_filling_details':
            return developer_filling_details(request, current_profile)
        elif request.user.profile.stage == 'recruiter_filling_details':
            return recruiter_filling_details(request, current_profile)
        elif request.user.profile.stage == 'complete':
            if request.user.profile.user_type == 'developer':
                try:
                    student = Student.objects.get(user_id=request.user.id)
                    passedquizz = TakenQuiz.objects.filter(score__gt=50).filter(student_id=student)
                    return render(request, 'frontend/developer/developer.html', {'passedquizz': passedquizz})
                except Student.DoesNotExist:
                    obj = Student(user=request.user)
                    obj.save()
                    return render(request, 'frontend/developer/developer.html')
            elif request.user.profile.user_type == 'recruiter':
                jobs = Job.objects.filter(posted_by=request.user)
                return render(request, 'frontend/recruiter/recruiter.html', {'transactions': transactions,'jobs':jobs})
    else:
        return home(request)


def home(request):
    return render(request, 'frontend/landing.html')


@login_required
def activity(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user)
        opencalls =OpenCall.objects.filter(recruiter=request.user)
        alltransactions =[]
        allopencalls =[]
        for transaction in transactions:
            alltransactions.append(transaction.id)
        for opencall in opencalls:
            allopencalls.append(opencall.transaction.id)

        res=set(alltransactions)-set(allopencalls)

        closedprojects =list(res)


        if request.user.profile.user_type == 'recruiter':
            return render(request, 'frontend/recruiter/my-activity.html', {'transactions': transactions,'closedprojects':closedprojects,'allopencalls':allopencalls})
        elif request.user.profile.user_type == 'developer':
            return render(request, 'frontend/developer/my-activity.html', {'transactions': transactions})

@login_required
def tracker(request, id):
    project = Transaction.objects.get(id=id)
    candidates = candidatesprojects.objects.filter(transaction=id)
    submitted = submissions.objects.filter(transaction=id).all()
    return render(request, 'frontend/recruiter/tracker.html', {'candidates': candidates, 'project': project,'submitted':submitted})


@login_required
def inprogress(request):
    user = request.user.id
    projects = candidatesprojects.objects.filter(candidate=user)
    return render(request, 'frontend/developer/inprogress.html', {'projects': projects})


@login_required
def invites(request):
    candidates = Candidate.objects.filter(email=request.user.email)
    return render(request, 'frontend/developer/invites.html', {'candidates': candidates})


@login_required
def projectdetails(request, id):
    form=Submissions()
    transaction=candidatesprojects.objects.get(id=id)
    projectinvite = Projectinvite()
    if Applications.objects.filter(candidate_id=request.user.id).filter(transaction_id=transaction.transaction_id).exists():
        opencall =Applications.objects.filter(candidate_id=request.user.id).filter(transaction_id=transaction.transaction_id).get()
    else:
        opencall=None
    project = candidatesprojects.objects.get(id=id)
    return render(request, 'frontend/developer/projectdetails.html',
                  {'project': project, 'projectinvite': projectinvite,'opencall':opencall,'form':form})


@login_required
def pendingproject(request, transaction_id):
    acceptedinvites = candidatesprojects.objects.filter(transaction_id=transaction_id, candidate=request.user)
    transaction = Transaction.objects.get(id=transaction_id)

    return render(request, 'frontend/developer/pendingproject.html',
                  {'transaction': transaction, 'acceptedinvites': acceptedinvites})

@login_required
def projectinvites(request, transaction_id):
    user = request.user.id
    trans_id = Transaction.objects.get(id=transaction_id)
    currentcandidate = User.objects.get(id=user)

    acceptedinvite = candidatesprojects(transaction=trans_id, candidate=currentcandidate, stage='invite-accepted')
    acceptedinvite.save()
    return redirect('frontend:buildproject')

@login_required
def update_candidateprojects(request, candidateproject_id, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    candidatesproject = candidatesprojects.objects.get(id=candidateproject_id)
    candidatesproject.stage = 'project-in-progress'
    candidatesproject.save()
    return HttpResponseRedirect('/projectdetails/%s' % candidateproject_id)

@login_required
def update_finished(request, candidateproject_id, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    candidatesproject = candidatesprojects.objects.get(id=candidateproject_id)
    candidatesproject.stage = 'project-completed'
    candidatesproject.save()
    return HttpResponseRedirect('/projectdetails/%s' % candidateproject_id)

@login_required
def update_finishedopencall(request, project_id, transaction_id):
    if request.method == 'POST':
        submission_form = Submissions(request.POST)
        if submission_form.is_valid():
            transaction = Transaction.objects.get(id=transaction_id)

            subject = 'Project submission'
            repo=submission_form.cleaned_data['repositorylink']
            demo = submission_form.cleaned_data['demolink']
            html_message = render_to_string('invitations/email/submissions.html',
                                            {'dev': request.user, 'transaction': transaction,'demo':demo,'repo':repo})
            plain_message = strip_tags(html_message)
            from_email = 'codeln@codeln.com'
            to = 'dennis@codeln.com'
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            candidatesproject = candidatesprojects.objects.get(id=project_id)
            candidatesproject.stage = 'project-completed'
            candidatesproject.save()
            submit = submissions(candidate=request.user,transaction=transaction,demo=demo,repo=repo)
            submit.save()
    return HttpResponseRedirect('/projectdetails/%s' % project_id)

def pricing(request):
    return render(request, 'frontend/pricing.html')


def dev(request):
    return render(request, 'frontend/dev.html')

def competitions(request):
    return render(request, 'frontend/recruiter/competitions.html')

def takenquizzes(request):
    taken = TakenQuiz.objects.all()
    allquizzes = TakenQuiz.objects.filter(score__gte=50).all()

    return render(request, 'frontend/recruiter/takenquizzes.html',{'allquizzes':allquizzes,'taken':taken})

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
                    dev.email = alluser.email
                    dev.firstname = alluser.first_name
                    dev.lastname = alluser.last_name
                    dev.language = alluser.profile.language
                    dev.framework = alluser.profile.framework
                    dev.country = alluser.profile.country
                    dev.github = alluser.profile.github_repo
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
                    recruiter.email = alluser.email
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
    developers = devs.objects.all()
    return render(request, 'frontend/recruiter/devlist.html', {'developers': developers})


def seerecruiters(request):
    payers = recruiters.objects.all()
    return render(request, 'frontend/recruiter/recruiterslist.html', {'payers': payers})

@login_required
def manageprojects(request):
    projects = Project.objects.all()
    return render(request, 'frontend/recruiter/projects.html', {'projects': projects})

@login_required
def managetransactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'frontend/recruiter/transactions.html', {'transactions': transactions})

@login_required
def editproject(request, project_id):
    instance = get_object_or_404(Project, id=project_id)
    project = Project.objects.get(id=project_id)
    form = EditProjectForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('frontend:manageprojects')

    return render(request, 'frontend/recruiter/editproject.html',
                  {'project': project, 'form': form})

@login_required
def deleteproject(request, project_id):
    Project.objects.filter(id=project_id).delete()
    return redirect('frontend:manageprojects')
@login_required
def addproject(request):
    form = EditProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('frontend:manageprojects')
    return render(request, 'frontend/recruiter/addproject.html',
                  { 'form': form})

@login_required
def edittransactions(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    candidates =Candidate.objects.filter(transaction_id=transaction_id)
    return render(request, 'frontend/recruiter/edittransaction.html',{'transaction':transaction,'candidates':candidates})
@login_required
def deletetransaction(request,transaction_id):
    OpenCall.objects.filter(transaction_id=transaction_id).delete()
    Transaction.objects.filter(id=transaction_id).delete()
    Candidate.objects.filter(transaction_id=transaction_id).delete()
    return redirect('frontend:managetransactions')
def closetransaction(request,transaction_id):
    project = Transaction.objects.get(id=transaction_id)
    project.closed = True
    project.save()
    return redirect('frontend:managetransactions')
@login_required
def buildproject(request):
    return render(request, 'classroom/students/worldprojects.html')
@login_required
def calltoapply(request):
    alltransactions=Transaction.objects.filter(stage='complete').filter(closed=False)
    complete=[]
    for i in alltransactions:
        complete.append(i.id)

    opportunities = OpenCall.objects.all()
    opencalls=[]
    for io in opportunities:
        opencalls.append(io.transaction.id)

    payedopencalls = set(complete)&set(opencalls)
    payed = list(payedopencalls)

    qualifys = Applications.objects.filter(candidate=request.user)
    student = Student.objects.get(user_id=request.user.id)
    passedquizz = TakenQuiz.objects.filter(score__gte=50).filter(student_id=student)

    allsubjectspassed = []
    for d in passedquizz:
        allsubjectspassed.append(d.quiz.subject)

    uniquesubjects = list(set(allsubjectspassed))
    uniquelangs=[]
    langs = {}
    for unique in uniquesubjects:
        izzes = TakenQuiz.objects.filter(quiz__subject_id=unique.id).filter(student_id=student)

        for i in izzes:
            langs[i.quiz.subject.name] = i.quiz.subject.name
    original =[]
    taken = []
    for oppo in payed:
        original.append(oppo)
    for qualify in qualifys:
        taken.append(qualify.transaction.id)
    untaken=[]

    non = set(original) - set(taken)
    untaken=list(non)
    untakenopportunities =[]
    for untake in untaken:
        untakentrans =Transaction.objects.get(id=untake)
        untakenopportunities.append(untakentrans.id)

    return render(request, 'classroom/students/opencalls.html',{'opportunities':opportunities,
                                                                'qualifys':qualifys,'a':original,'taken':taken,'untaken':untaken,'langs':langs,'qualify':qualifys})
@login_required
def apply(request,opportunity_id):
    language =OpenCall.objects.get(transaction=opportunity_id)
    student = Student.objects.get(user_id=request.user.id)
    passedquizz = TakenQuiz.objects.filter(score__gte=50).filter(student_id=student)


    allsubjectspassed = []
    for d in passedquizz:
        allsubjectspassed.append(d.quiz.subject)

    uniquesubjects = list(set(allsubjectspassed))


    for pa in uniquesubjects:
        blu=TakenQuiz.objects.filter(quiz__subject=pa).filter(student_id=student)
        doublequizzes =[]
        for paz in blu:
            doublequizzes.append(paz.score)


        if pa.name == language.transaction.framework.language.name or  pa.name == language.transaction.framework.name:  #TODO: let it be explcitly for framework if pa.name==language.project.framework
            qualifiedcandidate = Applications(recruiter=language.recruiter,transaction=language.transaction,project=language.project,candidate=request.user,stage='application sent',score=max(doublequizzes))

            qualifiedcandidate.save()




    return redirect('frontend:calltoapply')
@login_required
def opencalltracker(request,trans_id):
    candidatespicked = Candidate.objects.filter(transaction_id=trans_id)

    candidates = Applications.objects.filter(transaction=trans_id).order_by('-score')
    return render(request,'frontend/recruiter/opencall.html',{'candidates':candidates,'trans_id':trans_id,'picked':candidatespicked})
@login_required
def pickcandidates(request,trans_id,candidate_id):
    candidate =User.objects.get(id=candidate_id)
    transaction =Transaction.objects.get(id=trans_id)
    application= Applications.objects.filter(transaction = trans_id).filter(candidate_id=candidate_id).get()
    application.stage = 'accepted'
    newcandidate=Candidate(email=application.candidate.email,first_name=application.candidate.first_name,last_name=application.candidate.last_name,transaction=transaction)
    newcandidate.save()
    application.save()
    subject = 'Accepted for next stage'
    html_message = render_to_string('invitations/email/opencallaccepted.html',
                                    {'dev': request.user,'company':transaction})
    plain_message = strip_tags(html_message)
    from_email = 'codeln@codeln.com'
    to = candidate.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return HttpResponseRedirect('/opencalltracker/%s' % trans_id)


@login_required
def portfolio(request):
    try:
        candidate = Github.objects.get(candidate=request.user)
        user = candidate.github_username
        username = config('GITHUB_USERNAME',default='GITHUB_USERNAME')
        token = config('ACCESS_TOKEN',default='ACCESS_TOKEN')
        json_data = requests.get('https://api.github.com/users/' + user, auth=(username, token)).json()

        form = Portfolio_form()
        experience_form = Experience_Form()
        repo = 'https://api.github.com/users/' + user + '/repos'
        repos = requests.get(repo, auth=(username, token)).json()
        paginator = Paginator(repos, 8)

        page = request.GET.get('page')
        repoz = paginator.get_page(page)
        languages = []

        for i in repos:
            for x in i:
                languages.append(i['language'])

        counter = Counter(languages)
        labels = []
        c = {}
        items = []
        for z in counter:
            c[z] = counter[z]
            labels.append(z)
            items.append(counter[z])
        data = {
            "labels": labels,
            "data": items,
        }
        student = Student.objects.get(user_id=request.user.id)
        verified_skills = TakenQuiz.objects.filter(student=student).filter(score__gte=50).all()
        skill=[]
        for verified_skill in verified_skills:
            skill.append(verified_skill.quiz.subject.name)
        skillset=set(skill)
        skills =list(skillset)



        experiences=Experience.objects.filter(candidate=request.user).all()
        verified_projects = Portfolio.objects.filter(candidate=request.user).all()
        return render(request, 'frontend/developer/portfolio.html',
                      {'json': json_data, 'repos': repoz, 'data': data, 'c': c, 'form': form,
                       'verified_projects': verified_projects,'experience_form':experience_form,'experiences':experiences,'skills':skills})
    except Github.DoesNotExist:
        form = Github_form()

        return render(request, 'frontend/developer/github.html',{'form':form})


@login_required
def newproject(request):
    if request.method == 'POST':
        myprojects = Portfolio_form(request.POST)
        if myprojects.is_valid():
            title = myprojects.cleaned_data['title']
            description = myprojects.cleaned_data['description']
            image = myprojects.cleaned_data['image']
            repo = myprojects.cleaned_data['repository_link']
            demo = myprojects.cleaned_data['demo_link']
            newprojo =Portfolio(candidate=request.user,demo_link=demo,repository_link=repo,title=title,image=image,description=description)
            newprojo.save()
    return redirect(reverse('frontend:portfolio'))
@login_required
def get_data(request, *args, **kwargs):
    try:
        candidate = Github.objects.get(candidate=request.user)
        user = candidate.github_username
        username = config('GITHUB_USERNAME',default='GITHUB_USERNAME')
        token = config('ACCESS_TOKEN',default='ACCESS_TOKEN')
        repo = 'https://api.github.com/users/' + user + '/repos'
        repos = requests.get(repo, auth=(username, token)).json()

        languages = []
        for i in repos:
            for x in i:
                languages.append(i['language'])
        counter = Counter(languages)
        labels = []
        items = []
        for z in counter:
            labels.append(z)
            items.append(counter[z])
        data = {
            "labels": labels,
            "data": items,
        }

        return JsonResponse(data)


    except Github.DoesNotExist:
        form = Github_form()

        return render(request, 'frontend/developer/github.html',{'form':form})

def github(request):
    if request.method == 'POST':
        newuser = Github_form(request.POST)
        if newuser.is_valid():
            username = newuser.cleaned_data['github_username']
            password =newuser.cleaned_data['password']

            if requests.get('https://api.github.com/users/' + username, auth=(username, password)):
                newgithubprofile = Github(candidate=request.user, github_username=username)
                newgithubprofile.save()
                return redirect(reverse('frontend:portfolio'))
            else:


                return redirect(reverse('frontend:portfolio'))

    return redirect(reverse('frontend:portfolio'))
def experience(request):
    if request.method == 'POST':
        new_experience = Experience_Form(request.POST)
        if new_experience.is_valid():
            title = new_experience.cleaned_data['title']
            company = new_experience.cleaned_data['company']
            description = new_experience.cleaned_data['description']
            location = new_experience.cleaned_data['location']
            duration = new_experience.cleaned_data['duration']
            experience = Experience(candidate=request.user,title=title,description=description,company=company,location=location,duration=duration)
            experience.save()
            return redirect(reverse('frontend:portfolio'))
        else:
            return redirect(reverse('frontend:portfolio'))


    return redirect(reverse('frontend:portfolio'))

@login_required
def editportfolioproject(request,project_id):
    instance = get_object_or_404(Portfolio, id=project_id)
    project = Portfolio.objects.get(id=project_id)
    form = Portfolio_form(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('frontend:portfolio')

    return render(request, 'frontend/developer/editproject.html',{'project': project,'form':form})


