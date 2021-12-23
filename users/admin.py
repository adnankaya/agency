from django.contrib import admin

from users.models import Profile, SocialAccount

# Register your models here.
admin.site.register([Profile, SocialAccount])