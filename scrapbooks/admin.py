from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Scrapbook, Media

admin.site.register(Scrapbook)
admin.site.register(Media)