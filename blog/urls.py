from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('create_post/', views.create_or_edit_post, {}, name='create_post'),
    path('edit_post/<int:_id>/', views.create_or_edit_post, {}, name='edit_post'),
    path('', views.post_list, name='post_list'),
    path('post_detail/<int:post_id>', views.post_detail, name='post_detail'),
    path('tag/<str:tag_slug>/', views.post_list, name='post_list_by_tag'),
]
