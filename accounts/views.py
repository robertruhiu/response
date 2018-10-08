from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

@login_required
def profile(request, username=None):
    if username:
        u = User.objects.get(username=username)
        user = u
    else:
        user = request.user
    return render(request, 'accounts/profile.html', {'user': user})

