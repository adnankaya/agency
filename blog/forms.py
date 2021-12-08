from django import forms
# internals
from .models import Comment, Post


class PostForm(forms.Form):
    class Meta:
        model = Post
        fields = ('title', 'body', 'status', 'tags')


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('made_by', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()
