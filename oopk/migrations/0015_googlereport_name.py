# Generated by Django 4.1.4 on 2023-06-27 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oopk', '0014_alter_googlereport_spreadsheet_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='googlereport',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Наименование отчета'),
        ),
    ]