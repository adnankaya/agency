from django.contrib import admin

from core.models import Mail, Phone, Website

# Register your models here.
admin.site.register([Website, Mail, Phone])