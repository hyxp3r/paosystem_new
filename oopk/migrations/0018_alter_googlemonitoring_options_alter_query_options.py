# Generated by Django 4.1.4 on 2023-06-29 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oopk', '0017_query_googlemonitoring'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='googlemonitoring',
            options={'verbose_name': 'Мониторинг', 'verbose_name_plural': 'Мониторинг'},
        ),
        migrations.AlterModelOptions(
            name='query',
            options={'verbose_name': 'Запросы', 'verbose_name_plural': 'Запросы'},
        ),
    ]