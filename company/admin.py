from django.contrib import admin

from company.models import (
    About, AboutImage, Address, Contact, Milestone, Privacy, Service, ServiceImage, Terms, Client)

# Register your models here.
admin.site.register([Privacy, Terms, About, AboutImage, Milestone, Client,Contact,
                    Address, Service, ServiceImage])
