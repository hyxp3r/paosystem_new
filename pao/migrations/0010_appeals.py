# Generated by Django 4.1.4 on 2023-01-27 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pao', '0009_concat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appeals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Аппеляции')),
            ],
            options={
                'verbose_name': 'Аппеляции',
                'verbose_name_plural': 'Аппеляции',
            },
        ),
    ]