# Generated by Django 4.1.4 on 2023-07-02 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oopk', '0031_rename_query_query_query_body'),
    ]

    operations = [
        migrations.RenameField(
            model_name='query',
            old_name='query_body',
            new_name='body',
        ),
    ]
