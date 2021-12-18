from django.db import models
from django.db.models import Count


class PublishedManager(models.Manager):
    def get_queryset(self):
        qs = super(PublishedManager, self).get_queryset()
        qs = qs.filter(status='published').annotate(
            comment_count=Count('comments'))
        return qs


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(
            DraftManager,
            self).get_queryset().filter(status='draft')
