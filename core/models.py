from django.db import models


class Base(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = 'objects'


class Website(models.Model):
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=60, default='demosite')
    attributes = models.JSONField(null=True)
    logo = models.CharField(max_length=1024, null=True)

    class Meta:
        db_table = 't_website'
