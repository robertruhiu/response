from collections import Counter
from itertools import chain
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
from decouple import config
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail, serializers
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.response import Response
from rest_framework.views import APIView
from classroom.models import Student, TakenQuiz
from frontend.form import Portfolio_form, Experience_Form,CvForm
from frontend.models import Experience, Portfolio
from marketplace.filters import UserFilter
from .models import Job, JobApplication, DevRequest
from .forms import JobForm
from accounts.models import Profile
from django.utils.safestring import mark_safe
import json
from rest_framework.permissions import IsAuthenticated
from .serializers import DevRequestSerializer,JobRequestSerializer,JobApplicationsRequestSerializer
from rest_framework import generics

class DevRequestlist(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = DevRequestSerializer
    def get_queryset(self):

        user_id = self.kwargs['pk']
        dev = self.kwargs['dev']
        user=User.objects.get(id=user_id)


        try:
            dev_list = []
            dev_req = DevRequest.objects.filter(owner=user, paid=False, closed=False).get()
            for onedev in dev_req.developers:
                dev_list.append(onedev)
            dev_list.append(str(dev))
            dev_req.developers = dev_list
            dev_req.save()
            return DevRequest.objects.all()


        except DevRequest.DoesNotExist:
            devlist = []
            devlist.append(dev)
            dev_req = DevRequest(owner=user, paid=False, closed=False, developers=devlist)
            dev_req.save()
            return DevRequest.objects.all()


class Alldevsrequests(generics.RetrieveAPIView):
    queryset = DevRequest.objects.all()
    serializer_class = DevRequestSerializer
    lookup_field = 'owner'

class Myjobapplication(generics.ListAPIView):
    serializer_class = JobApplicationsRequestSerializer
    def get_queryset(self):
        job_id = self.kwargs['job']
        candidate_id = self.kwargs['candidate']
        job = Job.objects.get(id=job_id)
        user = User.objects.get(id=candidate_id)
        return JobApplication.objects.filter(job=job).filter(candidate=user)


class JobsList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobRequestSerializer


class Myjobsrequests(generics.ListAPIView):
    serializer_class = JobRequestSerializer

    def get_queryset(self):

        user_id = self.kwargs['posted_by']
        user =User.objects.get(id=user_id)
        return Job.objects.filter(posted_by=user)
class Jobsapplicants(generics.ListAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        job_id = self.kwargs['job']
        job = Job.objects.get(id=job_id)
        return JobApplication.objects.filter(job=job)
class Specificjob(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobRequestSerializer

class SpecificJobsapplicants(generics.ListAPIView):
    serializer_class = JobApplicationsRequestSerializer

    def get_queryset(self):
        job_id = self.kwargs['job']
        job = Job.objects.get(id=job_id)
        return JobApplication.objects.filter(job=job)

class JobUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = JobRequestSerializer

class JobCreateUpdate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Job.objects.all()
    serializer_class = JobRequestSerializer

class PickReject(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationsRequestSerializer





def job_list(request):
    if request.user.is_authenticated:

        applied_list = []
        alljoblist = []
        alljobs = Job.objects.all().order_by('-updated')

        for one_job in alljobs:
            alljoblist.append(one_job.id)
        developer = request.user
        applied_jobs = JobApplication.objects.filter(candidate=developer)
        for one_applied in applied_jobs:
            applied_list.append(one_applied.job_id)
        availablejobs_list=list(set(alljoblist)-set(applied_list))
        availablejobs = Job.objects.filter(pk__in=availablejobs_list)

        instance = get_object_or_404(Profile, user_id=request.user.id)
        unsigned = request.GET.get("unsigned") == "true"
        context = dict(

            backend_form=CvForm(),
            unsigned=unsigned,
            jobs=availablejobs,
            applied_jobs=applied_jobs,



        )
        if request.method == 'POST':
            # Only backend upload should be posting here
            form = CvForm(request.POST or None, request.FILES, instance=instance)
            context['posted'] = form.instance
            if form.is_valid():
                form.save()
    else:
        jobs = Job.objects.all().order_by('-updated')
        context = dict(
            jobs=jobs

        )
    return render(request, 'frontend/jobs.html', context)

@login_required
def job_details(request, id):
    job = Job.objects.get(id=id)

    selected_candidates = []
    applicants = []
    selected_devs = JobApplication.objects.filter(selected=True,job=job).all()
    for selectdev in selected_devs:
        selected_candidates.append(selectdev.candidate)
    all_devs = JobApplication.objects.filter(selected=False,job=job).all()
    for alldev in all_devs:
        applicants.append(alldev.candidate)

    # recommended=Profile.objects.filter(profile_tags__icontains=job.tech_stack.lower())



    alldevs = []


    listofdevs=list(set(alldevs))

    recommended=User.objects.filter(pk__in=listofdevs)
    return render(request, 'marketplace/recruiter/jobs/detail.html',
                      {'job': job, 'applicants': applicants, 'recommended': recommended,
                       'selected_candidates': selected_candidates})


@login_required
def create_or_edit_job(request, _id=None):
    if _id:
        job = get_object_or_404(Job, pk=_id)
        if job.posted_by != request.user:
            return HttpResponseForbidden()
    else:
        job = Job(posted_by=request.user)

    job_form = JobForm(data=request.POST or None, instance=job)

    if request.POST and job_form.is_valid():
        new_job = job_form.save(commit=False)
        new_job.save()

        return HttpResponseRedirect(reverse('marketplace:manage_posted_jobs'))


    return render(request, 'marketplace/recruiter/jobs/create.html', {'job_form': job_form,'job': mark_safe(json.dumps(job.description))})


@login_required
def apply_for_job(request, job_id):
    job=Job.objects.get(id=job_id)
    if request.method == 'POST':
        newapply = JobApplication(candidate=request.user, job=job)
        newapply.save()

        subject = job.title + 'Application sent by' + request.user.first_name + request.user.last_name
        html_message = render_to_string('invitations/email/jobapplications.html',
                                        {'dev': request.user,'job':job})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = 'jobs@codeln.com'
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        job = Job.objects.get(id=job_id)
        subject = 'Application received'
        html_message = render_to_string('invitations/email/applynotifiy.html',
                                        {'dev': request.user, 'job': job})
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = [request.user.email]
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return redirect(reverse('marketplace:job_list'))
    else:
        return redirect(reverse('marketplace:job_list'))

@login_required
def manage_posted_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    job_details = []
    for job in jobs:
        applied = JobApplication.objects.filter(job_id=job.id).all()
        app = applied.count()
        selected = JobApplication.objects.filter(job_id=job.id).filter(selected=True).all()
        sele = selected.count()
        job_details.append((job, app, sele))

    return render(request, 'marketplace/recruiter/jobs/list.html', {'job_details': job_details})

@login_required
def pick_candidate(request, job_id, dev_id):
    job = Job.objects.get(id=job_id)
    dev = User.objects.get(id=dev_id)
    newpick = JobApplication(job=job, candidate=dev, selected=True)
    newpick.save()
    subject = 'Shortlisted for job'
    html_message = render_to_string('invitations/email/accepted.html',
                                    {'dev': dev, 'job': job})
    plain_message = strip_tags(html_message)
    from_email = 'codeln@codeln.com'
    to = [dev.email]
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)


    return HttpResponseRedirect(reverse('marketplace:recruiter_job_detail', args=(job_id,)))

@login_required
def select_candidate(request, job_id, dev_id):
    candidate = User.objects.get(id=dev_id)
    job = JobApplication.objects.filter(job_id=job_id).filter(candidate=candidate).get()
    job.selected = True
    job.save()
    subject = 'Shortlisted for job'
    html_message = render_to_string('invitations/email/accepted.html',
                                    {'dev': candidate, 'job': job})
    plain_message = strip_tags(html_message)
    from_email = 'codeln@codeln.com'
    to = [candidate.email]
    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    job.selected = True
    job.save()
    return redirect('marketplace:job_details', job_id)


@login_required
def get_recommended_developers(job):

    developers = User.objects.filter(profile__user_type='developer').filter(
        profile__profile_tags__icontains=job.tech_stack.lower()).distinct()

    return developers

@login_required
def dev_pool(request):
    try:
        dev_req = DevRequest.objects.filter(owner=request.user, paid=False, closed=False).get()
        devcount = dev_req.developers
        requestcount = len(devcount)

        picked=[]
        for one_dev in dev_req.developers:

            picked.append(int(one_dev))
        picked_devs=User.objects.filter(pk__in=picked)
        developers_list = User.objects.filter(profile__user_type='developer').exclude(pk__in=picked)


        experiences = Experience.objects.all()
        verified_projects = Portfolio.objects.all()
        paginator = Paginator(developers_list, 25)
        page = request.GET.get('page')
        developers = paginator.get_page(page)
        return render(request, 'marketplace/recruiter/dev_pool.html',
                      {'developers': developers, 'experiences': experiences, 'projects': verified_projects,'picked':picked_devs,
                       'dev_count': mark_safe(json.dumps(requestcount))})
    except DevRequest.DoesNotExist:
        developers_list=User.objects.filter(profile__user_type='developer')
        experiences = Experience.objects.all()
        verified_projects = Portfolio.objects.all()
        paginator = Paginator(developers_list, 25)
        page = request.GET.get('page')
        developers = paginator.get_page(page)
        return render(request, 'marketplace/recruiter/dev_pool.html',
                  {'developers': developers,'experiences':experiences,'projects':verified_projects})
@login_required

def dev_data(APIVIEW):

    developers = User.objects.filter(profile__user_type='developer')

    dev_data={}
    experience=[]
    project=[]
    for dev in developers:
        experiences = Experience.objects.filter(candidate_id=dev.id)
        for work in experiences:
            experience.append(work)
        verified_projects = Portfolio.objects.filter(candidate_id=dev.id)
        for one_project in verified_projects:
            project.append(one_project)
        dev_data[dev]=[experience,project]

    data = {
        'title':'dennis'
    }


    return Response(data)


@login_required
def dev_details(request, dev_id):
    dev_picked = False


    requested_dev = User.objects.get(id=dev_id)
    try:
        student = Student.objects.get(user_id=dev_id)
    except Student.DoesNotExist:
        student = None


    verified_skills = TakenQuiz.objects.filter(student=student).filter(score__gte=50).all()
    skill = []
    for verified_skill in verified_skills:
        skill.append(verified_skill.quiz.subject.name)
    skillset = set(skill)
    skills = list(skillset)

    experiences = Experience.objects.filter(candidate=requested_dev).all()
    verified_projects = Portfolio.objects.filter(candidate=requested_dev).all()
    return render(request, 'marketplace/recruiter/dev_portfolio.html',
                  {
                   'verified_projects': verified_projects,
                   'experiences': experiences, 'skills': skills, 'developer': requested_dev,
                   'dev_picked': dev_picked})


@login_required()
def add_dev_to_wish_list(request):
    if request.method == 'GET':
        dev_id = request.GET['dev_id']
        try:
            dev_list=[]
            dev_req = DevRequest.objects.filter(owner=request.user, paid=False, closed=False).get()
            for onedev in dev_req.developers:
                dev_list.append(onedev)
            dev_list.append(str(dev_id))
            dev_req.developers=dev_list
            dev_req.save()
            count = len(dev_req.developers)
            data = {
                'dev_count': count
            }
            return JsonResponse(data)
        except DevRequest.DoesNotExist:
            devlist = []
            devlist.append(dev_id)
            dev_req = DevRequest(owner=request.user, paid=False, closed=False, developers=devlist)
            dev_req.save()
            count = len(dev_req.developers)
            dev_count = {
                'dev_count':count
            }

            return JsonResponse(dev_count)


    else:
        return HttpResponse("Request method is not a GET")


@login_required()
def process_payment(request):


    dev_req = DevRequest.objects.filter(paid=False,closed=False,owner=request.user).get()
    amount = len(dev_req.developers) * 20




    return render(request, 'marketplace/recruiter/payment.html',
                  {'amount': amount, 'transaction': dev_req})


@csrf_exempt
def payment_canceled(request):
    return redirect(reverse('marketplace:dev_pool'))


@csrf_exempt
def payment_done(request):
    dev_req = DevRequest.objects.get(closed=False,paid=False,owner=request.user)
    dev_req.paid = True
    dev_req.closed = True
    dev_req.save()
    email=[]
    for onedev in dev_req.developers:
        email.append(onedev.id)
    print(email)
    # send_mail(
    #     'Test invitation',
    #     'Hello' + ' ' + dev_req.dev.first_name + ' ' + dev_req.dev.last_name + ' ' + 'you have been invited by a Recruiter to partake in a test. '
    #                                                                                  'Use this link to login and access the test invite under Invites: http://beta.codeln.com/accounts/login/',
    #     'codeln@codeln.com',
    #     [dev_req.dev.email],
    #     fail_silently=False,
    # )

    return render(request, 'transactions/invitations.html',
                  {'candidates': dev_req.dev, 'current_transaction': dev_req})
@login_required
def mydevs(request):
    mydevs =DevRequest.objects.filter(owner=request.user)
    devs=[]
    for alldevspaidfor in mydevs:
        for onedev in alldevspaidfor.developers:
            devs.append(int(onedev))
    alldevs=list(set(devs))
    developers = User.objects.filter(pk__in=alldevs)

    return render(request, 'marketplace/recruiter/paid.html',{'developers':developers})

@login_required
def paid_dev_details(request, dev_id):
    try:
        student = Student.objects.get(user_id=dev_id)
    except Student.DoesNotExist:
        student = None


    requested_dev = User.objects.get(id=dev_id)

    verified_skills = TakenQuiz.objects.filter(student=student).filter(score__gte=50).all()
    skill = []
    for verified_skill in verified_skills:
        skill.append(verified_skill.quiz.subject.name)
    skillset = set(skill)
    skills = list(skillset)

    experiences = Experience.objects.filter(candidate=requested_dev).all()
    verified_projects = Portfolio.objects.filter(candidate=requested_dev).all()
    return render(request, 'marketplace/recruiter/paidprofiles.html',
                  {
                   'verified_projects': verified_projects,
                   'experiences': experiences, 'skills': skills, 'developer': requested_dev,
                   })
