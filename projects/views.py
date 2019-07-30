from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from marketplace.models import Job
from projects.forms import FrameworkForm
from projects.models import Project,Projecttype,Devtype,Framework
from rest_framework.permissions import IsAuthenticated
from .serializers import Projectserializer
from rest_framework import generics
import random
from django.contrib.auth.models import User
from marketplace.models import JobApplication,DevRequest
from accounts.models import Profile
class Projects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        job_id = self.kwargs['id']
        job = Job.objects.get(id=job_id)
        projects = Project.objects.all()
        tags = job.tech_stack.split(",")
        randomlist =[]
        for oneproject  in projects :
            for onetag in tags:
                if oneproject.tags.find(onetag.lower()):
                    randomlist.append(oneproject.id)
        print(randomlist)
        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]


        return Project.objects.filter(pk=projectid)

class RecommendedProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = User.objects.get(pk=user_id)
        userprofile = Profile.objects.get(user=user)
        projects = Project.objects.all()
        tags = userprofile.skills.split(",")
        randomlist =[]
        for oneproject  in projects :
            for onetag in tags:
                if oneproject.tags.find(onetag.lower()):
                    randomlist.append(oneproject.id)
        if len(randomlist) > 0:
            projectid = random.choice(randomlist)
        else:
            projectid = randomlist[0]

        return Project.objects.filter(pk=projectid)

class Allprojects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = Projectserializer

class ProjectDetails(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = Projectserializer

class RecentProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = User.objects.get(pk=user_id)
        recentprojects = JobApplication.objects.filter(recruiter=user)[:2]
        project_ids = []
        for oneproject in recentprojects:
            project_ids.append(oneproject.project.id)
        return Project.objects.filter(pk__in=project_ids)
class MyRecentProjects(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Projectserializer
    def get_queryset(self):
        user_id = self.kwargs['id']
        user = User.objects.get(pk=user_id)
        recentprojects = DevRequest.objects.filter(owner=user)[:2]
        project_ids = []
        for oneproject in recentprojects:
            project_ids.append(oneproject.project)
        return project_ids







# Create your views here.
# def project_categories(request):
#     # list all project categories
#     if request.method == 'GET':
#         return render(request, 'projects/categories.html', {})
#     elif request.method == 'POST':
#         return HttpResponse('<h2> Done </h2>')


# def project_category_list(request):
#     # list all project from above category
#     # filter projects by framework, language
#     pass

@login_required
def project_list(request,type_id):
    # TODO: filter projects by framework, language and category using django filter
    categoryname=Projecttype.objects.get(id=type_id)

    projecttypes = Project.objects.filter(projecttype_id=type_id)
    return render(request, 'projects/all_projects.html', {'projecttypes': projecttypes,'categoryname':categoryname})
@login_required
def devtypes(request,dev_id):
    # TODO: filter projects by framework, language and category using django filter

    categoryname=Devtype.objects.get(id=dev_id)
    devtypes = Project.objects.filter(devtype_id=dev_id)
    return render(request, 'projects/devtypes.html', {'devtypes':devtypes,'categoryname':categoryname})
@login_required
def categories(request):
    projecttypes = Projecttype.objects.all()
    devtypes = Devtype.objects.all()

    return render(request, 'projects/categories.html',{'projecttypes':projecttypes, 'devtypes': devtypes})

@login_required
def project(request, id):

    frameworks =Framework.objects.all()
    project = Project.objects.get(id=id)
    framework_form = FrameworkForm()
    return render(request, 'projects/project.html', {'project': project,'frameworks':frameworks,'framework_form':framework_form,})
