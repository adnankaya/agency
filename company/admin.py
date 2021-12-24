from django.contrib import admin

from company.models import (
    About, AboutImage, Address, ContactMessage, Milestone, Privacy, Service, ServiceImage, Terms, Client)

# Register your models here.
admin.site.register([Privacy, Terms, About, AboutImage, Milestone, Client,ContactMessage,
                    Address, Service, ServiceImage])
