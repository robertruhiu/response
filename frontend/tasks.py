from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.core import mail
@shared_task
def reminderforprofiledevs(request):
    allusers = User.objects.all()
    for dev in allusers:
        if dev.profile.user_type =='developer' and dev.profile.stage == 'complete' and dev.email == 'codeln@codeln.com':
            subject = 'Reminder'
            html_message = render_to_string('invitations/email/reminder.html' ,{'dev':dev})
            plain_message = strip_tags(html_message)
            from_email = 'noreply@sandbox3921b04244fe414a8168eb9e0bc3e8ae.mailgun.org'
            to = dev.email

            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return redirect('frontend:index')
