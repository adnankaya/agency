from django.db import models

class Base(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    class Meta:
        abstract = True
        default_manager_name = 'objects'