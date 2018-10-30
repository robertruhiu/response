"""codelnmain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from frontend.views import index
from frontend.views import activity,tracker,inprogress,invites,projectdetails,pendingproject,dev,recruit

app_name = 'frontend'
urlpatterns = [
    path('', index, name='index'),
    path('tracker', tracker, name='tracker'),
    path('dev', dev, name='dev'),
    path('recruit', recruit, name='recruit'),
    path('inprogress', inprogress, name='inprogress'),
    path('invites', invites, name='invites'),
    path('pendingproject', pendingproject, name='pendingproject'),
    path('projectdetails', projectdetails, name='projectdetails'),
    path('activity/', activity, name='my-activity'),

]
