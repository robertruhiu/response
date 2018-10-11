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
from .views import process_payment, payment_done, payment_canceled

# TODO: create payment handlers for paypal, flutterwave, paystack etc

app_name = 'payments'

urlpatterns = [
    # the id here is transaction id
    path('pay/<int:id>/', process_payment, name='pay'),
    path('done/<int:id>/', payment_done, name='done'),
    path('canceled/<int:id>/', payment_canceled, name='canceled'),
]

# paystack urls
urlpatterns += [
    #path()
]
