# Generated by Django 2.0.1 on 2018-06-17 20:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('processor', '0002_auto_20180617_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='uri',
            name='uploader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
