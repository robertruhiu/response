from django.urls import path

from blog.views import create_or_edit_post,post_detail,post_list

app_name = 'blog'

urlpatterns = [
    path('create_post/',create_or_edit_post,  name='create_post'),
    path('edit_post/<int:_id>/',create_or_edit_post,  name='edit_post'),
    path('', post_list, name='post_list'),
    path('post_detail/<int:post_id>', post_detail, name='post_detail'),

]
