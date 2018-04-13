from django.contrib import admin

from .models import *


class DoiAdmin(admin.ModelAdmin):
    list_display = ('doi', 'last_checked')
admin.site.register(Doi, DoiAdmin)


class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'doi')
admin.site.register(Url, UrlAdmin)


class DoiUploadAdmin(admin.ModelAdmin):
    list_display = ('doi', 'upload')
admin.site.register(DoiUpload, DoiUploadAdmin)


class ScrapeAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date')
admin.site.register(Scrape, ScrapeAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('doi', 'source', 'created_at', 'scrape')
admin.site.register(Event, EventAdmin)
