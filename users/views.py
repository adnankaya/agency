from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.translation import gettext as _
from django.views.generic.edit import View
from django.contrib.auth.models import User
# internals
from .forms import CustomUserLoginForm, CustomUserCreationForm
from core.models import Website


def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            msg = _('{} is registered successfully. You can log in!'.format(username))
            messages.success(request, msg)
            return redirect('users:login')
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
        user = user = authenticate(request, username=username, password=raw_pass)
        login(request, user)
        return redirect("/")
    context = {
        'form': form,
        'website': Website.objects.first()
    }
    return render(request, "users/login.html", context)


def reset_password(request):
    return HttpResponse('Reset Password #TODO')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
