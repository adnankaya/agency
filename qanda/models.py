from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

from publish.models import Publish
# internal
from core.utils import generate_slug


class Question(Publish):
    text = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 't_qanda'

    def __str__(self):
        return self.text
