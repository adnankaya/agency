from django.shortcuts import render, get_object_or_404
from django.core.paginator import (Paginator,
                                   EmptyPage,
                                   PageNotAnInteger)
# Create your views here.
from .models import Service


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
