# Generated by Django 4.1.2 on 2022-12-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pao', '0004_alter_department_shortname'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ('name',), 'verbose_name': 'Отдел', 'verbose_name_plural': 'Отдел'},
        ),
        migrations.AlterField(
            model_name='contractnames',
            name='sectionEC',
            field=models.CharField(max_length=10, verbose_name='Номер пункта'),
        ),
    ]
