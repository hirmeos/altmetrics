from django import forms

from s3direct.widgets import S3DirectWidget


class CSVUploadForm(forms.Form):

    csv = forms.URLField(
        widget=S3DirectWidget(dest='custom_filename')
    )
