from django.contrib import admin

from company.models import (
    About, AboutImage, Address, Milestone, Privacy, Service, ServiceImage, Terms)

# Register your models here.
admin.site.register([Privacy, Terms, About, AboutImage, Milestone,
                    Address, Service, ServiceImage])
