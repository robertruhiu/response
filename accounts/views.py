from django.contrib import messages
from django.db import transaction
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.forms import ProfileEditForm, UserEditForm, DeveloperProfileEditForm, RecruiterProfileEditForm
from django.shortcuts import render, redirect
from accounts.models import Profile


# Create your views here.

@login_required
def profile(request, pk=None):
    if pk:
        u = User.objects.get(id=pk)
        user = u
    else:
        user = request.user
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def update_profile(request):
    if request.user.profile.user_type == 'developer':

        if request.method == 'POST':

            profile_form = DeveloperProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():

                profile_form.save()
                # messages.success(request, ('Your profile was successfully saved'))
                return redirect('frontend:index')
            else:
                print('Failed')
                # messages.error(request, ('Please correct the error below.'))
        else:

            profile_form = DeveloperProfileEditForm(instance=request.user.profile)
            return render(request, 'frontend/profile_edit_form.html',
                          {'profile_form': profile_form})
    elif request.user.profile.user_type == 'recruiter':
        if request.method == 'POST':

            profile_form = RecruiterProfileEditForm(request.POST, instance=request.user.profile)
            if  profile_form.is_valid():

                profile_form.save()
                # messages.success(request, ('Your profile was successfully saved'))
                return redirect('frontend:index')
            else:
                print('Failed')
                # messages.error(request, ('Please correct the error below.'))
        else:

            profile_form = RecruiterProfileEditForm(instance=request.user.profile)
            return render(request, 'frontend/profile_edit_form.html',
                          { 'profile_form': profile_form})
