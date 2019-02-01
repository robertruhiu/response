from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.core import mail
from classroom.models import TakenQuiz
from transactions.models import Applications
import csv

@shared_task
def reminderforprofiledevs(request):
    allusers = User.objects.all()
    for dev in allusers:
        if dev.profile.user_type =='developer' and dev.profile.stage == 'developer_filling_details':
            subject = 'Reminder'
            html_message = render_to_string('invitations/email/reminder.html' ,{'dev':dev})
            plain_message = strip_tags(html_message)
            from_email = 'codeln@codeln.com'
            to = dev.email
            mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return render(request, 'frontend/recruiter/recruiter.html')

def applyreminder(request):
    passed_set = TakenQuiz.objects.filter(score__gte=50)
    all = []
    for pas in passed_set:
        all.append(pas.student.user.email)
    myset = set(all)

    taken = []
    applied = Applications.objects.all()
    for i in applied:
        taken.append(i.candidate.email)
    send_email = set(all) - set(taken)
    emails = list(send_email)
    for email in emails:
        subject = 'Profile meets requirements'
        html_message = render_to_string('invitations/email/applyreminder.html')
        plain_message = strip_tags(html_message)
        from_email = 'codeln@codeln.com'
        to = email
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

    return render(request, 'frontend/recruiter/recruiter.html')


def massmail(request):
    mails =[]
    with open('frontend/static/frontend/mail.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            mails.append(row)
    cleanlist=[]
    for email in mails:
        cleanlist.append(email[0])
    print(cleanlist)
    csvFile.close()
    registerd =[]
    currentusers=User.objects.all()
    for user in currentusers:
        registerd.append(user.email)
    unregistered =set(cleanlist)-set(registerd)
    print(unregistered)
    return render(request, 'frontend/recruiter/recruiter.html')


