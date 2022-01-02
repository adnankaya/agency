import markdown
from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
# internals
from ..models import Client, Milestone, Service

register = template.Library()


@register.simple_tag
def get_services():
    return Service.objects.prefetch_related('serviceimage_set')


@register.simple_tag
def get_milestones():
    return Milestone.objects.order_by('date_in')


@register.simple_tag
def get_clients():
    return Client.objects.all()
