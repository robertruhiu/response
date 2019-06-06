from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from projects.forms import FrameworkForm
from projects.models import Project,Projecttype,Devtype,Framework



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
