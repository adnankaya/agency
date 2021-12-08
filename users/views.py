from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.utils.translation import gettext as _
from django.views.generic.edit import View
# internals
from .forms import CustomUserLoginForm, CustomUserCreationForm


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
        'form': form
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form = CustomUserLoginForm(request.POST or None)
    if form.is_valid():
        user_obj = form.cleaned_data.get("user_obj")
        login(request, user_obj)
        return redirect("/")
    return render(request, "users/login.html", {"form": form})


def reset_password(request):
    return HttpResponse('Reset Password #TODO')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
