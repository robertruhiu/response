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
from .views import process_payment, payment_canceled, flutterwavepayment_done,process_opencalloption1,process_opencalloption2,process_opencalloption3

app_name = 'payments'

urlpatterns = [
    path('pay/<int:id>/', process_payment, name='pay'),
    path('opencall1/<int:id>/', process_opencalloption1, name='payoption1'),
    path('opencall2/<int:id>/', process_opencalloption1, name='payoption2'),
    path('opencall3/<int:id>/', process_opencalloption1, name='payoption3'),

    path('canceled/<int:id>/', payment_canceled, name='canceled'),
    path('flutterdone/<int:id>/', flutterwavepayment_done, name='flutter-done'),
]


# flutterwave confirmation url
