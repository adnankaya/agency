from django.db import models
from taggit.managers import TaggableManager

from core.models import Base
from django.utils import timezone
from django.contrib.auth.models import User


class Publish(Base):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="%(app_label)s_%(class)s_related")
    published_date = models.DateTimeField(default=timezone.now)

    tags = TaggableManager()

    class Meta:
        abstract = True
        ordering = ('-published_date',)
