from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.forms import (UserCreationForm,)


class CustomUserLoginForm(forms.Form):
    query = forms.CharField(label=_('username or email'))
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')

        user_qs_final = User.objects.filter(
            Q(username__iexact=query) |
            Q(email__iexact=query)
        ).distinct()

        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError(_('User not exist!'))
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError(_('username or password is wrong!'))
        self.cleaned_data["user_obj"] = user_obj
        return super(CustomUserLoginForm, self).clean(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, label=_("Email"),
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        help_text=_("Enter your email.")
    )

    class Meta:
        model = User
        fields = ('username', 'email')
