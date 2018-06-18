from django.contrib import admin

from .models import Uri, Url, UriUpload, Scrape, Event


class UriAdmin(admin.ModelAdmin):

    list_display = ('raw', 'last_checked')


class UrlAdmin(admin.ModelAdmin):

    list_display = ('url', 'uri')


class UriUploadAdmin(admin.ModelAdmin):

    list_display = ('uri', 'upload')


class ScrapeAdmin(admin.ModelAdmin):

    list_display = ('start_date', 'end_date')


class EventAdmin(admin.ModelAdmin):

    list_display = ('uri', 'measure', 'created_at', 'scrape')


admin.site.register(Uri, UriAdmin)
admin.site.register(Url, UrlAdmin)
admin.site.register(UriUpload, UriUploadAdmin)
admin.site.register(Scrape, ScrapeAdmin)
admin.site.register(Event, EventAdmin)
