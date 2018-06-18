from django.contrib import admin

from .models import CSVUpload

class CSVUploadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'user', 'date_uploaded', 'processed')

admin.site.register(CSVUpload, CSVUploadAdmin)