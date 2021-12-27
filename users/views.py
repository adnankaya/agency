from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.translation import gettext as _
from django.views.generic.edit import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.urls import reverse_lazy

# internals
from .forms import CustomUserLoginForm, CustomUserCreationForm
from core.models import Website
from .forms import (UserUpdateForm, ProfileUpdateForm)
from .tokens import get_account_activation_token


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and get_account_activation_token().check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/email_confirmation_done.html')
    else:
        return HttpResponse('Activation link is invalid!')


def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            _template = 'users/activate_user.html'
            url = reverse_lazy('users:activate',
                               kwargs={
                                   'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                                   'token': get_account_activation_token().make_token(user),
                               })
            activate_url = '{}{}'.format(current_site.domain, url)
            _context = {
                'user': user,
                'activate_url': activate_url,
            }
            mail_subject = _('Activate your account.')
            message = render_to_string(_template, _context)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            return render(request, 'users/email_confirmation.html')
    context = {
        'form': form,
        'website': Website.objects.first()
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = CustomUserLoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        raw_pass = form.cleaned_data.get("password")
        user = user = authenticate(
            request, username=username, password=raw_pass)
        login(request, user)
        return redirect("/")
    context = {
        'form': form,
        'website': Website.objects.first()
    }
    return render(request, "users/login.html", context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your account has been updated!'))
            return redirect('users:profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }

    return render(request, 'users/profile.html', context)
