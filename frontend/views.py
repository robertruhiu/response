from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.core.paginator import Paginator
from collections import Counter
from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import TruncMonth
import requests
from datetime import date,datetime,time
from django.core.mail import send_mail
import json
from decouple import config
from rest_framework.permissions import IsAuthenticated
import base64
import urllib.parse
from django.contrib import messages
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from accounts.forms import ProfileTypeForm, DeveloperFillingDetailsForm, RecruiterFillingDetailsForm,Profile
from transactions.models import Transaction, Candidate,OpenCall,Applications
from invitations.models import Invitation
from projects.models import Project, Framework
from frontend.form import Projectinvite, EditProjectForm,Submissions,Portfolio_form,Experience_Form,About,GradingForm
from frontend.models import candidatesprojects,submissions,Portfolio,Experience,Report
from classroom.models import TakenQuiz,Student,Quiz
from marketplace.models import Job
from .serializers import UserSerializer,ProfileSerializer,ExperienceSerializer,ProjectSerializer
from rest_framework import generics, permissions

class UserList(generics.ListAPIView):

    serializer_class = ProfileSerializer

    def get_queryset(self):

        return Profile.objects.filter(user_type='developer')

class AllUsers(generics.ListAPIView):

    serializer_class = UserSerializer

    def get_queryset(self):

        return User.objects.all()



class Talentget(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class Portfolioget(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer

    def get_queryset(self):
        candidate_id = self.kwargs['candidate_id']
        user = User.objects.get(id=candidate_id)
        return Portfolio.objects.filter(candidate_id=user)




class Experienceget(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExperienceSerializer

    def get_queryset(self):

        candidate_id = self.kwargs['candidate_id']
        user = User.objects.get(id=candidate_id)
        return Experience.objects.filter(candidate=user)


class AllPortfolioget(generics.ListAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = ProjectSerializer


class AllExperienceget(generics.ListAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class Profileget(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class Userget(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

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
            current_profile.csa = developer_filling_details_form.cleaned_data['csa']
            current_profile.about = developer_filling_details_form.cleaned_data['about']

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
                    # if request.user.profile.profile_tags == None:
                    #     tags = []
                    #     frameworks = Profile.objects.get(user_id=request.user.id)
                    #     tags = []
                    #     if frameworks:
                    #         if 'react' in frameworks.framework.lower():
                    #             tags.insert(0, True)
                    #         else:
                    #             tags.insert(0, False)
                    #         if 'vue' in frameworks.framework.lower():
                    #             tags.insert(1, True)
                    #         else:
                    #             tags.insert(1, False)
                    #         if 'angular' in frameworks.framework.lower():
                    #             tags.insert(2, True)
                    #         else:
                    #             tags.insert(2, False)
                    #         if 'express' in frameworks.framework.lower():
                    #             tags.insert(3, True)
                    #         else:
                    #             tags.insert(3, False)
                    #         if 'laravel' in frameworks.framework.lower():
                    #             tags.insert(4, True)
                    #         else:
                    #             tags.insert(4, False)
                    #         if 'django' in frameworks.framework.lower():
                    #             tags.insert(5, True)
                    #         else:
                    #             tags.insert(5, False)
                    #         if 'net' in frameworks.framework.lower():
                    #             tags.insert(6, True)
                    #         else:
                    #             tags.insert(6, False)
                    #         if 'flutter' in frameworks.framework.lower():
                    #             tags.insert(7, True)
                    #         else:
                    #             tags.insert(7, False)
                    #         if 'android' in frameworks.framework.lower():
                    #             tags.insert(8, True)
                    #         else:
                    #             tags.insert(8, False)
                    #         if 'ionic' in frameworks.framework.lower():
                    #             tags.insert(9, True)
                    #         else:
                    #             tags.insert(9, False)
                    #         if 'java' in frameworks.language.lower():
                    #             tags.insert(10, True)
                    #         else:
                    #             tags.insert(10, False)
                    #         if 'c++' in frameworks.language.lower():
                    #             tags.insert(11, True)
                    #         else:
                    #             tags.insert(11, False)
                    #         if 'c#' in frameworks.language.lower():
                    #             tags.insert(12, True)
                    #         else:
                    #             tags.insert(12, False)
                    #     dev_tags = Profile.objects.get(user_id=request.user.id)
                    #     dev_tags.profile_tags = tags
                    #     dev_tags.save()
                    #
                    #     return render(request, 'frontend/developer/developer.html', {'passedquizz': passedquizz})
                    # else:
                    return render(request, 'frontend/developer/developer.html', {'passedquizz': passedquizz})

                except Student.DoesNotExist:
                    obj = Student(user=request.user)
                    obj.save()
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
    candidates = candidatesprojects.objects.filter(transaction=id).order_by('-stage')
    submitted = submissions.objects.filter(transaction=id).all()
    readyreports = Report.objects.filter(transaction_id=id)
    reports=[]

    for on in readyreports:
        reports.append(on.candidate_id)
    allcandidates=[]
    for one in candidates:
        allcandidates.append(one.candidate_id)
    withoutreports = list(set(allcandidates) - set(reports))
    candswithreports =Report.objects.filter(transaction_id=id).order_by('-score')

    candwithoutreports=candidatesprojects.objects.filter(candidate_id__in=withoutreports,transaction_id=id).order_by('-stage')




    return render(request, 'frontend/recruiter/tracker.html', {'candswithreports': candswithreports,'candwithoutreports': candwithoutreports, 'project': project,'submitted':submitted,'readyreports':readyreports,
                                                               'cands':candidates})


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



def passedquizzes(request):
    taken = TakenQuiz.objects.all()
    return render(request, 'frontend/recruiter/takenquizzes.html',{'taken':taken})
def failedquizzes(request):
    taken = TakenQuiz.objects.all()
    return render(request, 'frontend/recruiter/failed.html',{'taken':taken})

def howitworks(request):
    return render(request, 'frontend/how.html')


def report(request,candidate_id,transaction_id):
    user = User.objects.get(id=candidate_id)
    report =Report.objects.get(candidate_id=candidate_id,transaction_id=transaction_id)
    transaction = Transaction.objects.get(id=transaction_id)
    print(type(report.keycompitency[0]))
    return render(request, 'frontend/recruiter/report.html', {'user': user, 'transaction': transaction,'report':report})


def onboarddevs(request):


    return redirect(reverse('frontend:seedevs'))


def onboardrecruiters(request):


    return redirect(reverse('frontend:seerecruiters'))


def credits(request):
    return render(request, 'frontend/credits.html')


def privacy(request):
    return render(request, 'frontend/privacy.html')


def terms(request):
    return render(request, 'frontend/terms.html')


def sample(request):
    return render(request, 'frontend/sample.html')


def page_404(request,exception=None):
    return render(request, 'frontend/error_pages/404.html')


def page_500(request):
    return render(request, 'frontend/error_pages/500.html')


def seedevs(request):

    developers=User.objects.filter(profile__user_type='developer').order_by('-date_joined')


    return render(request, 'frontend/recruiter/devlist.html', {'developers': developers})


def seerecruiters(request):

    recruiters = User.objects.filter(profile__user_type='recruiter').order_by('-date_joined')


    return render(request, 'frontend/recruiter/recruiterslist.html', {'payers': recruiters})

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
    candidates =candidatesprojects.objects.filter(transaction_id=transaction_id).order_by('-stage')
    withreports=Report.objects.filter(transaction_id=transaction_id)
    reports=[]
    without=[]
    for onewithreport in withreports:
        reports.append(onewithreport.candidate_id)
    for all in candidates:
        without.append(all.candidate_id)

    withoutreportslist=list(set(without)-set(reports))
    withoutreport=candidatesprojects.objects.filter(candidate_id__in=withoutreportslist,transaction_id=transaction_id).order_by('-stage')
    return render(request, 'frontend/recruiter/edittransaction.html',{'transaction':transaction,'candidates':withreports,'withoutreport':withoutreport})
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
    for onetransaction in alltransactions:
        complete.append(onetransaction)

    allopencalls = OpenCall.objects.all()
    opencalls=[]
    for oneopencall in allopencalls:
        opencalls.append(oneopencall.transaction)

    payedopencalls = set(complete)&set(opencalls)
    payed = list(payedopencalls)

    opencallapplied = Applications.objects.filter(candidate=request.user)
    applied=[]
    for opencall in opencallapplied:
        applied.append(opencall.transaction)
    opportunities=list(set(payed)-set(applied))

    student = Student.objects.get(user_id=request.user.id)
    takenquizzes = TakenQuiz.objects.filter(student_id=student)
    allquizid=[]
    for two in takenquizzes:
        allquizid.append(two.quiz.id)


    allsubjectstaken = []
    for onequiz in takenquizzes:
        allsubjectstaken.append(onequiz.quiz.subject)

    uniquesubjects = list(set(allsubjectstaken))
    langs = {}
    for unique in uniquesubjects:
        allstudentquizzes = TakenQuiz.objects.filter(quiz__subject_id=unique.id).filter(student_id=student)

        for onestudentquiz in allstudentquizzes:
            langs[onestudentquiz.quiz.subject.name] = onestudentquiz.quiz.subject.name
    passedquizzes = TakenQuiz.objects.filter(score__gte=50).filter(student_id=student)
    passedquizid=[]
    for one in passedquizzes:
        passedquizid.append(one.quiz.id)
    quizzes = Quiz.objects.all()
    qualified = {}
    unqualified ={}
    for onepassedquiz in passedquizzes:
        for opportunity in opportunities:
            if opportunity.framework.name == onepassedquiz.quiz.name:
                qualified[opportunity]=onepassedquiz
    qualifiedtransactions=[]
    for key,value in qualified.items():
        qualifiedtransactions.append(key)
    unqualifiedtransactions =list(set(opportunities)-set(qualified))

    openopportunities ={}
    for oneunqualified in unqualifiedtransactions:
        for quizmoja in quizzes:
            if oneunqualified.framework.name == quizmoja.name:
                openopportunities[oneunqualified]=quizmoja


    return render(request, 'classroom/students/opencalls.html',{'opportunities':opportunities,
                                                                'opencallapplied':opencallapplied,
                                                                'langs':langs,'quizzes':quizzes,'passedquizzes':passedquizzes,'qualified':qualified,
                                                                'unqualifiedtransactions':openopportunities})
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


        if pa.name == language.transaction.framework.name:
            qualifiedcandidate = Applications(recruiter=language.recruiter,transaction=language.transaction,
                                              project=language.project,candidate=request.user,stage='application sent',score=max(doublequizzes))

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
                                    {'dev': candidate,'company':transaction})
    plain_message = strip_tags(html_message)
    from_email = 'codeln@codeln.com'
    to = candidate.email
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return HttpResponseRedirect('/opencalltracker/%s' % trans_id)


@login_required
def portfolio(request):
    form = Portfolio_form()
    experience_form = Experience_Form()
    about_form = About()

    student = Student.objects.get(user_id=request.user.id)
    verified_skills = TakenQuiz.objects.filter(student=student).filter(score__gte=50).all()
    skill = []
    for verified_skill in verified_skills:
        skill.append(verified_skill.quiz.subject.name)
    skillset = set(skill)
    skills = list(skillset)

    experiences = Experience.objects.filter(candidate=request.user).all()
    verified_projects = Portfolio.objects.filter(candidate=request.user).all()
    return render(request, 'frontend/developer/portfolio.html',
                  {'form': form,
                   'verified_projects': verified_projects, 'experience_form': experience_form,
                   'experiences': experiences,
                   'skills': skills, 'about_form': about_form})

@login_required
def newproject(request):
    if request.method == 'POST':
        myprojects = Portfolio_form(request.POST)
        if myprojects.is_valid():
            title = myprojects.cleaned_data['title']
            description = myprojects.cleaned_data['description']
            repo = myprojects.cleaned_data['repository_link']
            demo = myprojects.cleaned_data['demo_link']
            newprojo =Portfolio(candidate=request.user,demo_link=demo,repository_link=repo,title=title,description=description)
            newprojo.save()
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




def competitions(request):
    qualifys={}
    try:
        transaction =Transaction.objects.get(user_id=760)
        if request.user.is_authenticated:
            try:
                hi = Applications.objects.get(candidate=request.user, transaction_id=transaction.id)
                qualifys=hi
            except Applications.DoesNotExist:
                qualifys = None
    except Transaction.DoesNotExist:
        transaction=None
    quiz = Quiz.objects.get(id=12)
    passedquizzes={}
    if request.user.is_authenticated:

        if request.user.profile.user_type=='developer':
            student = Student.objects.get(user_id=request.user.id)
            try:
                passedquizzes = TakenQuiz.objects.get(score__gte=50,student_id=student.id,quiz_id=12)
            except TakenQuiz.DoesNotExist:
                passedquizzes=None

    return render(request, 'frontend/recruiter/competitions.html',{'transaction':transaction,
                                                                   'qualify':qualifys,'passedquizzes':passedquizzes,'quiz':quiz})
@login_required
def placeapplication(request,transaction_id):
    language =OpenCall.objects.get(transaction=transaction_id)
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
            subject = 'Application received'
            message = ' Thank you for placing your application. \n ' \
                      'You will soon get an invite to conduct further assessment by a Codeln representative \n' \
                      '\n' \
                      'Cheers team Codeln '
            email_from = config('EMAIL_HOST_USER', default='EMAIL_HOST_USER')
            to = request.user.email
            send_mail(subject, message, email_from, [to])

    return redirect('frontend:competitions')
def about(request):
    instance = get_object_or_404(Profile,user_id=request.user.id)
    if request.method =='POST':
        new_about = About(request.POST or None,instance=instance)
        if new_about.is_valid():
            new_about.save()
            return redirect('frontend:portfolio')
    return redirect(reverse('frontend:portfolio'))
def management(request):
    jobs=Job.objects.all()

    return render(request, 'frontend/recruiter/management.html',{'jobs':jobs})
def grading(request,candidate_id,transaction_id):
    candidate = User.objects.get(id=candidate_id)
    transaction = Transaction.objects.get(id=transaction_id)
    gradingform = GradingForm()
    return render(request, 'frontend/recruiter/grading.html',{'candidate':candidate,'transaction':transaction,'form':gradingform })


def storegrades(request,candidate_id,transaction_id):
    candidate = User.objects.get(id=candidate_id)
    transaction = Transaction.objects.get(id=transaction_id)
    requirements = []
    keycompitency = []
    grading = []
    if request.method == 'POST':
        form = GradingForm(request.POST)

        requirement1 = request.POST.get('requirement1', False);
        requirement2 = request.POST.get('requirement2', False);
        requirement3 = request.POST.get('requirement3', False);
        requirement4 = request.POST.get('requirement4', False);
        requirement5 = request.POST.get('requirement5', False);
        requirement6 = request.POST.get('requirement6', False);
        requirement7 = request.POST.get('requirement7', False);
        requirement8 = request.POST.get('requirement8', False);
        requirement9 = request.POST.get('requirement9', False);
        requirement10 = request.POST.get('requirement10', False);

        requirements.insert(0, requirement1)
        requirements.insert(1, requirement2)
        requirements.insert(2, requirement3)
        requirements.insert(3, requirement4)
        requirements.insert(4, requirement5)
        requirements.insert(5, requirement6)
        requirements.insert(6, requirement7)
        requirements.insert(7, requirement8)
        requirements.insert(8, requirement9)
        requirements.insert(9, requirement10)

        deliverables = request.POST.get('deliverables', False);
        errors = request.POST.get('errors', False);
        security = request.POST.get('security', False);
        readability = request.POST.get('readability', False);

        keycompitency.insert(0, deliverables)
        keycompitency.insert(1, errors)
        keycompitency.insert(2, security)
        keycompitency.insert(3, readability)

        passed = request.POST.get('passed', False);
        failed = request.POST.get('failed', False);
        vulnerable = request.POST.get('vulnerable', False);
        errors = request.POST.get('errors', False);
        lines = request.POST.get('lines', False);
        duplications = request.POST.get('duplications', False);
        classes = request.POST.get('classes', False);
        comments = request.POST.get('comments', False);
        depedencies = request.POST.get('depedencies', False);
        debt = request.POST.get('debt', False);
        gates = request.POST.get('gates', False);

        grading.insert(0, passed)
        grading.insert(1, failed)
        grading.insert(2, vulnerable)
        grading.insert(3, errors)
        grading.insert(4, lines)
        grading.insert(5, duplications)
        grading.insert(6, classes)
        grading.insert(7, comments)
        grading.insert(8, depedencies)
        grading.insert(9, debt)
        grading.insert(10, gates)
        github = request.POST.get('github', False);
        score = request.POST.get('score', False);
        print(score)
        obj = Report(candidate=candidate, transaction=transaction, requirements=requirements,
                     keycompitency=keycompitency, grading=grading, score=score,github=github)
        obj.save()


    return redirect('frontend:edittransactions', transaction_id)
def analytics(request):
    passedtests = TakenQuiz.objects.filter(score__gte=50).annotate(month=TruncMonth('date')).values(
        'month').annotate(
        total=Count('student_id'))
    faileddataset=[]
    passeddatasets=[]
    alltestdataset=[]
    developersdataset=[]
    recruitersdataset=[]
    for one in passedtests:
        timevalue=''
        totalvalue=''
        for key, value in one.items():
            if key =='month':
                timevalue=value
            if key =='total':
                totalvalue=value
        passeddatasets.append([timevalue.year,timevalue.month,totalvalue])
    passed=(sorted(passeddatasets))







    failedtests= TakenQuiz.objects.filter(score__lt=50).annotate(month=TruncMonth('date')).values('month').annotate(
        total=Count('student_id'))
    for one in failedtests:
        timevalue=''
        totalvalue=''
        for key, value in one.items():
            if key =='month':
                timevalue=value
            if key =='total':
                totalvalue=value
        faileddataset.append([timevalue.year,timevalue.month,totalvalue])
    failed=(sorted(faileddataset))


    alltested = TakenQuiz.objects.annotate(month=TruncMonth('date')).values('month').annotate(
        total=Count('student_id'))
    for one in alltested:
        timevalue=''
        totalvalue=''
        for key, value in one.items():
            if key =='month':
                timevalue=value
            if key =='total':
                totalvalue=value
        alltestdataset.append([timevalue.year,timevalue.month,totalvalue])
    alltests=(sorted(alltestdataset))


    alldevelopers=User.objects.filter(profile__user_type='developer').annotate(month=TruncMonth('date_joined')).values('month').annotate(
        total=Count('id'))
    for one in alldevelopers:
        timevalue=''
        totalvalue=''
        for key, value in one.items():
            if key =='month':
                timevalue=value
            if key =='total':
                totalvalue=value
        developersdataset.append([timevalue.year,timevalue.month,totalvalue])
    developers=(sorted(developersdataset))

    allrecruiters = User.objects.filter(profile__user_type='recruiter').annotate(month=TruncMonth('date_joined')).values(
        'month').annotate(
        total=Count('id'))
    for one in allrecruiters:
        timevalue=''
        totalvalue=''
        for key, value in one.items():
            if key =='month':
                timevalue=value
            if key =='total':
                totalvalue=value
        recruitersdataset.append([timevalue.year,timevalue.month,totalvalue])
    recruiters=(sorted(recruitersdataset))

    return render(request, 'frontend/recruiter/analytics.html',{'passed':passed,'failed':failed,'alltests':alltests,'developers':developers,
                                                                'recruiters':recruiters})

