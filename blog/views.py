from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView

from .models import Post, Comment
from .forms import CommentForm, PostForm
from taggit.models import Tag
from django.db.models import Count
from django.utils.safestring import mark_safe
import json

def post_list(request):

    posts = Post.published.all()



    return render(request, 'blog/post/list.html', { 'posts': posts})


def post_detail(request, post_id):
    """a view to display details of a single post."""
    allposts=Post.objects.filter(status='published')
    post = get_object_or_404(
        Post,
        id=post_id
    )

    # active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # comment posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # don't save comment to database yet
            new_comment = comment_form.save(commit=False)

            # assign the current post to the comment
            new_comment.post = post

            # finally, save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()




    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form,'allposts':allposts })


@login_required
def create_or_edit_post(request, _id=None):
    if _id:
        post = get_object_or_404(Post, pk=_id)
        if post.author != request.user:
            return HttpResponseForbidden()
    else:
        post = Post(author=request.user)

    post_form = PostForm(data=request.POST or None, instance=post)

    if request.POST and post_form.is_valid():
        new_post = post_form.save(commit=False)
        new_post.save()

        return HttpResponseRedirect(reverse('blog:post_list'))


    return render(request, 'blog/post/create.html', {'post_form': post_form,'post': mark_safe(json.dumps(post.body))})


