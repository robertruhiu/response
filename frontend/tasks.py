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
from accounts.models import Profile
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
    angular = Profile.objects.filter(framework__contains='angular').filter(country='NG')
    react = Profile.objects.filter(framework__contains='react').filter(country='NG')
    mongo = Profile.objects.filter(framework__contains='Node').filter(country='NG')
    python = Profile.objects.filter(language__contains='python').filter(country='NG')
    golang = Profile.objects.filter(language__contains='golang').filter(country='NG')
    li=[55,
56,
550,
183,
399,
302,
405,
399,
299,
484,
397,
313,
55,
160,
183,
399,
228,
216,
637,
275,
302,
362,
496,
641,
533,
483,
472,
576,
560,
569,
53,
77,
231,
200,
209,
202,
196,
207,
252,
324,
311,
344,
336,
373,
347,
556,
466,
540,
495,
489,
571,
291,
482,
47,
635,
141,
204,
229,
637,
275,
396,
362,
376,
378,
373,
423,
443,
533,
483,
642,
53,
76,
86,
172,
231,
399,
198,
216,
250,
390,
319,
324,
322,
364,
391,
392,
359,
363,
434,
556,
464,
535,
564,
489,
371,
291,
585,
558,
302,
483,
472,
551
]
    newset = set(li)
    new =list(newset)
    me = []
    # for can in angular:
    #     li.append(can.user_id)
    # for can in react:
    #     li.append(can.user_id)
    for can in mongo:
        li.append(can.user_id)
    # for can in python:
    #     li.append(can.user_id)
    # for can in golang:
    #     li.append(can.user_id)
    # myset =set(li)
    # newlist = list(myset)
    nn =[]
    for m in new:
        casc = User.objects.get(id=m)
        nn.append(casc.email)
    for jsk in nn:
        print(jsk)


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
        subject = 'Mest Dev competition Submission Deadlines.'
        message = 'Hello ' + candidate.candidate.first_name + '.\n We hope you are having a great time on the project.' + \
              candidate.transaction.projecttitle + '\n \n Wanted to inform you that the final deadline for submission for the project is this Friday (8/March/2019) \n  We hope to see your development skills in your final product. \n' \
                                                           'Also join the conversation with fellow developers at the chat app in the right bottom corner.If you got an issue we will reply in the shortest time possible\n' \
                                                           'Cheers From Team Codeln'


        from_email = 'codeln@codeln.com'
        to = candidate.candidate.email
        mail.send_mail(subject, message, from_email, [to])
    for cand in submissions_mails:
        subject = 'Mest Dev competition Submission Deadlines.'
        message = 'Hello ' + cand.candidate.first_name + '.\n We hope you are having a great time on the project.' + \
                  cand.transaction.projecttitle + '\n \n Wanted to inform you that the final deadline for submission for the project is this Friday (8/March/2019) \n  We hope to see your development skills in your final product. \n' \
                                                               'Also join the conversation fellow developers at the chat app in the right bottom corner.If you got an issue we will reply in the shortest time possible\n' \
                                                               'Cheers From Team Codeln'

        from_email = 'codeln@codeln.com'
        to = cand.candidate.email
        mail.send_mail(subject, message, from_email, [to])
    return render(request, 'frontend/recruiter/recruiter.html')



