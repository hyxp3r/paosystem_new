# Generated by Django 4.1.4 on 2023-07-02 18:14

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('oopk', '0032_rename_query_body_query_body'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Airtable',
            new_name='AirtablePersonal',
        ),
    ]