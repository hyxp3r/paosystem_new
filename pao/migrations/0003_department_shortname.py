# Generated by Django 4.1.2 on 2022-12-29 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pao', '0002_alter_checkec_options_alter_contractnames_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='shortName',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Сокращенное название'),
        ),
    ]
