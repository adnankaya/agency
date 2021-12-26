from django.contrib import admin

# Register your models here.
from .models import Masthead

admin.site.register([
    Masthead
])
