from .models import Comment, Post
from django import forms
from taggit.forms import TagWidget

from ckeditor.widgets import CKEditorWidget
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class PostForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ('title', 'status', 'body','blogsplashimage')
        widgets = {
            'tags': TagWidget(),
        }

