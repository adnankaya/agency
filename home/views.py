from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.http.response import HttpResponseRedirect
from django.contrib import messages
# internals
from company.forms import ContactForm
from core.models import Website


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your message has been sent"))
            return HttpResponseRedirect('/')

    else:
        form = ContactForm()
    context = {
        'website':Website.objects.filter(is_active=True).last(),
        'form': form
    }
    return render(request, 'home/index.html', context)

