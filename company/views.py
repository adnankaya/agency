from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator,
                                   EmptyPage,
                                   PageNotAnInteger)
from django.http.response import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from company.forms import ContactForm
from .models import About, Contact, Privacy, Service, Terms


def services_list(request):
    allservices = Service.objects.prefetch_related('serviceimage_set')
    paginator = Paginator(allservices, per_page=12)
    page = request.GET.get('page')
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        services = paginator.page(number=1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        services = paginator.page(number=paginator.num_pages)
    context = {
        'services': services
    }
    return render(request, 'company/services/list.html', context)


def service_detail(request, slug):
    qset = Service.objects.prefetch_related('serviceimage_set')
    service = get_object_or_404(qset, slug=slug)
    context = {'service': service}
    return render(request, 'company/services/detail.html', context)


def about(request):
    context = {
        'about': About.objects.filter(is_deleted=False).last()
    }
    return render(request, 'company/about/index.html', context)


def privacy(request):
    context = {
        'privacy': Privacy.objects.last()
    }
    return render(request, 'company/privacy.html', context)


def terms(request):
    context = {
        'terms_obj': Terms.objects.last()
    }
    return render(request, 'company/terms.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Your message has been sent"))
            return HttpResponseRedirect('/')

    else:
        form = ContactForm()
    return render(request, 'home/index.html', {'form': form})
