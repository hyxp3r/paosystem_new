# Generated by Django 4.1.4 on 2023-01-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pao', '0008_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('email', models.EmailField(max_length=50)),
            ],
            options={
                'verbose_name': 'Контанкт',
                'verbose_name_plural': 'Контакт',
            },
        ),
    ]
