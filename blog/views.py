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


class PostListView(ListView):
    """a class-based view to display the list of posts."""
    queryset = Post.published.all()  # object list
    context_object_name = 'posts'  # context variable for query results, defaults to object_list
    paginate_by = 1  # number of posts per page
    template_name = 'blog/post/list.html'  # rendering template


def post_list(request, tag_slug=None):
    """a view to display the list of posts."""
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # number of posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # deliver first page if page is not an integer
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # deliver last page if page is out of range

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag})


def post_detail(request, post_id):
    """a view to display details of a single post."""
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

    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'comment_form': comment_form, 'similar_posts': similar_posts})


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
        new_post.slug = slugify(new_post.title)
        new_post.save()

        tags = post_form.cleaned_data['tags']
        new_post.tags.add(*tags)

        return HttpResponseRedirect(reverse('blog:post_list'))

    return render(request, 'blog/post/create.html', {'post_form': post_form})
