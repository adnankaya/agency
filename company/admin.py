from django.contrib import admin

from company.models import (
    About, AboutImage, Address, Privacy, Service, ServiceImage, Terms)

# Register your models here.
admin.site.register([Privacy, Terms, About, AboutImage,
                    Address, Service, ServiceImage])
