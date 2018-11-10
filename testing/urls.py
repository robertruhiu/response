from django.urls import path

from testing.views import start_project

app_name = 'testing'

urlpatterns = [
    path('start-project/<int:id>/', start_project, name='start-project'),
]
