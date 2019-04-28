from django.urls import path

from marketplace.views import job_list, job_details, apply_for_job, post_job, manage_posted_jobs, pick_candidate, \
    select_candidate, dev_pool, dev_details, process_payment, payment_canceled, payment_done, add_dev_to_wish_list,\
    mydevs,paid_dev_details

app_name = 'marketplace'

urlpatterns = [

    path('job_list/', job_list, name='job_list'),
    path('job_details/<int:id>/', job_details, name='job_details'),
    path('apply_for_job/<int:job_id>/', apply_for_job, name='apply_for_job'),

    path('post_job/', post_job, name='post_job'),
    path('manage_posted_jobs/', manage_posted_jobs, name='manage_posted_jobs'),
    path('pick_candidate/<int:job_id>/<int:dev_id>/', pick_candidate, name='pick_candidate'),
    path('select_candidate/<int:job_id>/<int:dev_id>/', select_candidate, name='select_candidate'),
    path('dev_pool/', dev_pool, name='dev_pool'),
    path('mydevs/', mydevs, name='mydevs'),
    path('dev_details/<int:dev_id>/<int:req_id>/', dev_details, name='dev_details'),
    path('paid_dev_details/<int:dev_id>', paid_dev_details, name='paid_dev_details'),
    path('add_dev_to_wish_list/<int:dev_id>/', add_dev_to_wish_list, name='add_dev_to_wish_list'),
    path('process_payment/<int:req_id>/', process_payment, name='process_payment'),
    path('payment_canceled/', payment_canceled, name='payment_canceled'),
    path('payment_done/<int:req_id>/', payment_done, name='payment_done'),
]
