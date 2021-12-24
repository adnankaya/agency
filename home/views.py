from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Prefetch
# internals
from company.forms import ContactMessageForm
from core.models import Mail, Phone, Website
from company.models import Address


def queryset_website():
    '''Fetch last active website and pre fetch mails and phones `display` is True '''
    return Website.objects.filter(is_active=True).prefetch_related(
        Prefetch('mails', queryset=Mail.objects.filter(display=True)),
        Prefetch('phones', queryset=Phone.objects.filter(display=True)),
        Prefetch('addresses', queryset=Address.objects.filter(display=True)),
    ).last()


def index(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your message has been sent"))
            return HttpResponseRedirect('/')

    else:
        form = ContactMessageForm()
    context = {
        'website': queryset_website(),
        'form': form
    }
    return render(request, 'home/index.html', context)
