from django.urls import path

from marketplace.views import job_list, job_details, apply_for_job, manage_posted_jobs, pick_candidate, \
    select_candidate, dev_pool, dev_details, process_payment, payment_canceled, payment_done, add_dev_to_wish_list,\
    mydevs,paid_dev_details,create_or_edit_job,dev_data,DevRequestlist,Alldevsrequests,Myjobsrequests,Jobsapplicants,\
    Specificjob,SpecificJobsapplicants,Myjobapplication,JobUpdate,JobCreateUpdate,JobsList,PickReject

app_name = 'marketplace'

urlpatterns = [

    path('job_list/', job_list, name='job_list'),
    path('job_details/<int:id>/', job_details, name='job_details'),
    path('apply_for_job/<int:job_id>/', apply_for_job, name='apply_for_job'),

    path('post_job/', create_or_edit_job, name='post_job'),
    path('edit_job/<int:_id>/',create_or_edit_job,  name='edit_job'),
    path('manage_posted_jobs/', manage_posted_jobs, name='manage_posted_jobs'),
    path('pick_candidate/<int:job_id>/<int:dev_id>/', pick_candidate, name='pick_candidate'),
    path('select_candidate/<int:job_id>/<int:dev_id>/', select_candidate, name='select_candidate'),
    path('dev_pool/', dev_pool, name='dev_pool'),
    path('dev_data/', dev_data, name='dev_data'),
    path('mydevs/', mydevs, name='mydevs'),
    path('dev_details/<int:dev_id>', dev_details, name='dev_details'),
    path('paid_dev_details/<int:dev_id>', paid_dev_details, name='paid_dev_details'),
    path('add_dev_to_wish_list', add_dev_to_wish_list, name='add_dev_to_wish_list'),
    path('process_payment', process_payment, name='process_payment'),
    path('payment_canceled', payment_canceled, name='payment_canceled'),
    path('payment_done', payment_done, name='payment_done'),
    path('devrequest/<int:pk>/<int:dev>', DevRequestlist.as_view()),
    path('alldevrequests/<int:owner>', Alldevsrequests.as_view()),
    path('myjobs/<int:posted_by>', Myjobsrequests.as_view()),
    path('jobapplicants/<int:job>', Jobsapplicants.as_view()),
    path('specificjob/<int:pk>', Specificjob.as_view()),
    path('specificjobapplicants/<int:job>', SpecificJobsapplicants.as_view()),
    path('updatejob/<int:pk>', JobUpdate.as_view()),
    path('pickreject/<int:pk>', PickReject.as_view()),
    path('createupdatejob', JobCreateUpdate.as_view()),
    path('alljobs', JobsList.as_view()),
    path('myjobapplication/<int:candidate>/<int:job>', Myjobapplication.as_view()),

]
