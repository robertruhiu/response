from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.core import mail
from classroom.models import TakenQuiz
from transactions.models import Applications
from frontend.models import candidatesprojects
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
def submission(request):
    invitations_mails=[]
    submissions_mails =[]
    emails = candidatesprojects.objects.all()
    for email in emails:
        if email.stage == 'invite-accepted':
            invitations_mails.append(email)
        elif email.stage == 'project-in-progress':
            submissions_mails.append(email)
    for candidate in invitations_mails:
        subject = 'Mest Dev competition.'
        message = 'Hello ' + candidate.candidate.first_name + '.\n We noticed you accepted an invitation for the competition.The deadline is creeping up for' + \
              candidate.transaction.user.profile.company + '\n \n Use this link to see the project you were assigned and see details concerning deliverables and submission guidelines \n  https://beta.codeln.com/inprogress/ \n' \
                                                           'Thank you'


        from_email = 'codeln@codeln.com'
        to = candidate.candidate.email
        mail.send_mail(subject, message, from_email, [to])
    for cand in submissions_mails:
        subject = 'Mest Dev competition.'
        message = 'Hello ' + cand.candidate.first_name + '.\n Thank you for being part of the competition.The deadline is creeping up for the ' + \
                  cand.transaction.user.profile.company + '.We hope to recieve your demo and github repo of the project assigned before the submission portal closes.\n \n  Use this link to see the project you were assigned and see details concerning deliverables and submission guidelines \n  https://beta.codeln.com/inprogress/ \n' \
                                                               'Thank you'

        from_email = 'codeln@codeln.com'
        to = cand.candidate.email
        mail.send_mail(subject, message, from_email, [to])
    return render(request, 'frontend/recruiter/recruiter.html')



