from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.core import mail
from classroom.models import TakenQuiz
from transactions.models import Applications,Transaction
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
    li=[
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
    # invitations_mails=[]
    # submissions_mails =[]
    # emails = candidatesprojects.objects.all()
    # for email in emails:
    #     if email.stage == 'invite-accepted':
    #         invitations_mails.append(email)
    #     elif email.stage == 'project-in-progress':
    #         submissions_mails.append(email)
    # for candidate in invitations_mails:
    #     subject = 'Project submission deadline update'
    #     html_message = render_to_string('invitations/email/mestsubmission.html',
    #                                     {'dev': candidate})
    #     plain_message = strip_tags(html_message)
    #     from_email = 'codeln@codeln.com'
    #     to = candidate.candidate.email
    #     mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    # candidates=Applications.objects.filter(transaction_id=95,stage='accepted')
    # for cand in candidates:
    #     subject = 'Book time'
    #     html_message = render_to_string('invitations/email/mestsubmission.html',
    #                                     {'dev': cand})
    #     plain_message = strip_tags(html_message)
    #     from_email = 'codeln@codeln.com'
    #     to = cand.candidate.email
    #     mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    # passedlist = TakenQuiz.objects.filter(score__gte=50)
    # failedlist =TakenQuiz.objects.filter(score__lt=50)
    # allpassed=[]
    # for student in failedlist:
    #     allpassed.append(student.student.user.email)
    # trimmed =set(allpassed)
    # kupita=list(trimmed)
    # print(*kupita, sep='\n')
    # # emails=User.objects.filter(id_in = kupita)
    # # passedemails =[]
    # # for email in emails:
    # #     print(email.email)
    # accepted=[]
    # pending=[]
    # transaction = Applications.objects.filter(stage='application sent',transaction_id=95)
    # for one in transaction:
    #     accepted.append([one.candidate.first_name+one.candidate.last_name,one.candidate.email])
    # print(*accepted,sep='\n')
    candidates=Profile.objects.filter(user_type='developer')
    for onecandidate in candidates:
        if onecandidate.profile_tags == None:
            tags = []
            frameworks = Profile.objects.get(user_id=onecandidate.user_id)
            tags = []
            if frameworks:
                if 'react' in frameworks.framework.lower():
                    tags.insert(0, 'reactjs')
                else:
                    tags.insert(0, False)
                if 'vue' in frameworks.framework.lower():
                    tags.insert(1, 'vuejs')
                else:
                    tags.insert(1, False)
                if 'angular' in frameworks.framework.lower():
                    tags.insert(2, 'angularjs')
                else:
                    tags.insert(2, False)
                if 'express' in frameworks.framework.lower():
                    tags.insert(3, 'expressjs')
                else:
                    tags.insert(3, False)
                if 'laravel' in frameworks.framework.lower():
                    tags.insert(4, 'laravel')
                else:
                    tags.insert(4, False)
                if 'django' in frameworks.framework.lower():
                    tags.insert(5, 'django')
                else:
                    tags.insert(5, False)
                if 'net' in frameworks.framework.lower():
                    tags.insert(6, True)
                else:
                    tags.insert(6, False)
                if 'flutter' in frameworks.framework.lower():
                    tags.insert(7, 'flutter')
                else:
                    tags.insert(7, False)
                if 'android' in frameworks.framework.lower():
                    tags.insert(8, 'android')
                else:
                    tags.insert(8, False)
                if 'ionic' in frameworks.framework.lower():
                    tags.insert(9, 'ionicjs')
                else:
                    tags.insert(9, False)
                if 'java' in frameworks.language.lower():
                    if 'javascript' in frameworks.language.lower():
                        tags.insert(10, False)
                    else:
                        tags.insert(10, 'java')
                else:
                    tags.insert(10, False)
                if 'c++' in frameworks.language.lower():
                    tags.insert(11, 'c++')
                else:
                    tags.insert(11, False)
                if 'c#' in frameworks.language.lower():
                    tags.insert(12, 'c#')
                else:
                    tags.insert(12, False)
            dev_tags = Profile.objects.get(user_id=onecandidate.user_id)
            dev_tags.profile_tags = tags
            dev_tags.save()


    return render(request, 'frontend/recruiter/recruiter.html')



