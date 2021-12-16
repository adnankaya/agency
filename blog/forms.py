from django import forms
from django.utils.translation import ugettext_lazy as _

# internals
from .models import Comment, Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = _('Title')
        self.fields['body'].label = _('Body')
        self.fields['status'].label = _('Status')
        self.fields['tags'].label = _('Tags')

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
    ALGORITHMS = (
        ("default", "DEFAULT"),
        ("weighting", "WEIGHTING"),
        ("trigram", "TRIGRAM"),
    )
    query = forms.CharField()
    search_algorithm = forms.ChoiceField(choices=ALGORITHMS, required=False)
