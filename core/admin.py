from django.contrib import admin

from core.models import Mail, Phone, SocialAccount, Website

# Register your models here.
admin.site.register([Website, Mail, Phone,SocialAccount])
