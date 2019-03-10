from django.urls import path

from marketplace.views import job_list,dev_job_detail,apply_for_job,post_job,manage_posted_jobs,recruiter_job_detail,pick_candidate,select_candidate

app_name = 'marketplace'

urlpatterns = [

    path('job_list/', job_list, name='job_list'),
    path('job_detail/<int:id>', dev_job_detail, name='dev_job_detail'),
    path('apply_for_job/<int:job_id>/', apply_for_job, name='apply_for_job'),

    path('post_job/', post_job, name='post_job'),
    path('manage_posted_jobs/', manage_posted_jobs, name='manage_posted_jobs'),
    path('job_detail/<int:id>/', recruiter_job_detail, name='recruiter_job_detail'),
    path('pick_candidate/<int:job_id>/<int:dev_id>/', pick_candidate, name='pick_candidate'),
    path('select_candidate/<int:job_id>/<int:dev_id>/', select_candidate, name='select_candidate'),
]
