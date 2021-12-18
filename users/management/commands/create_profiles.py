from typing import Any, Optional
from django.conf import settings
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        User = apps.get_model(settings.AUTH_USER_MODEL)
        Profile = apps.get_model('users', 'Profile')
        profiles = [Profile(user=user)
                    for user in User.objects.filter(profile=None)]
        Profile.objects.bulk_create(profiles)
