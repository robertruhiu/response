from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
class PublishedManager(models.Manager):
    """
    custom model manager for Post model.
    retrieves all posts with published status.
    """

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    objects = models.Manager()  # the default manager
    published = PublishedManager()  # customer manager for published posts

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    blogsplashimage=models.CharField(max_length=250)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='blog_posts')
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    class Meta:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

class Comment(models.Model):
    # associate comment with a particular post
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    # person commenting
    name = models.CharField(max_length=80)

    # person's email
    email = models.EmailField()

    # actual comment message
    body = models.TextField()

    # when comment was made
    created = models.DateTimeField(auto_now_add=True)

    # when comment was updated
    updated = models.DateTimeField(auto_now=True)

    # used to manually deactivate inappropriate comments on a post
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
