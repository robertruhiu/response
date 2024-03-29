from django.urls import path

from marketplace.views import job_list, job_details, apply_for_job, manage_posted_jobs, pick_candidate, \
    select_candidate, dev_pool, dev_details, process_payment, payment_canceled, payment_done, add_dev_to_wish_list,\
    mydevs,paid_dev_details,create_or_edit_job,dev_data,Myjobsrequests,Jobsapplicants,\
    Specificjob,SpecificJobsapplicants,Myjobapplication,JobUpdate,JobCreate,JobsList,PickReject,PickRecommended,JobUnpublish,\
    DevRequestpick,DevRequests,CandidateManager,MyApplicants,Jobdetails,JobApply,CandidateJobs

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
    path('mydevs/<int:owner>', DevRequests.as_view()),
    path('myapplicants/<int:owner>',MyApplicants.as_view()),
    path('pickdev', DevRequestpick.as_view()),
    path('myjobs/<int:posted_by>', Myjobsrequests.as_view()),
    path('jobapplicants/<int:job>', Jobsapplicants.as_view()),
    path('specificjob/<int:pk>', Specificjob.as_view()),
    path('specificjobapplicants/<int:job>', SpecificJobsapplicants.as_view()),
    path('updatejob/<int:pk>', JobUpdate.as_view()),
    path('unpublishjob/<int:pk>', JobUnpublish.as_view()),
    path('pickreject/<int:pk>', PickReject.as_view()),
    path('candidatemanager/<int:pk>', CandidateManager.as_view()),
    path('pickrecommended', PickRecommended.as_view()),
    path('createjob', JobCreate.as_view()),
    path('alljobs', JobsList.as_view()),
    path('myjobapplication/<int:candidate>/<int:job>', Myjobapplication.as_view()),
    path('jobdetails/<int:pk>', Jobdetails.as_view()),
    path('applyjob', JobApply.as_view()),
    path('candidatejobs/<int:candidate>', CandidateJobs.as_view()),

]
