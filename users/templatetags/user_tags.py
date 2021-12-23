from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
# internals
from ..models import User

register = template.Library()


@register.simple_tag
def get_team():
    qs = User.objects.filter(profile__has_team=True) \
        .select_related('profile') \
        .prefetch_related('socialaccounts')
    return qs
