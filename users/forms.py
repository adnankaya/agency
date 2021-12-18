from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm)

from users.models import Profile


class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _("Email")
        self.fields['email'].help_text = _('Enter your email.')

    class Meta:
        model = User
        fields = ('username', 'email')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = _("Email")
        # self.fields['email'].help_text = _('Enter your email.')

    class Meta:
        model = User
        fields = ('username', 'email')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
