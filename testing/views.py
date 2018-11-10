from django.shortcuts import render
from testing.tasks import digital_ocean


# Create your views here.

def start_project(request, id):
    digital_ocean(id=id)
    return render(request, 'testing/start-project.html')
