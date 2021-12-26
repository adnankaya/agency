from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
# internals
from ..models import Profile, User

register = template.Library()


@register.simple_tag
def get_team():
    qs = Profile.objects.filter(has_team=True) \
        .prefetch_related('socialaccounts')
    return qs
