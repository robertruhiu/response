from django.http import HttpResponse
from django.shortcuts import render
from projects.models import Project


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


def project_list(request):
    # TODO: filter projects by framework, language and category using django filter
    all_projects = Project.objects.all()
    return render(request, 'projects/all_projects.html', {'all_projects': all_projects})


def project(request, id):
    project = Project.objects.get(id=id)
    return render(request, 'projects/project.html', {'project': project})
