# Generated by Django 4.1.4 on 2023-08-02 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oopk', '0034_remove_airtablepersonal_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamesTite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Наименование')),
                ('group', models.BooleanField(default=False, verbose_name='Содержит группы?')),
                ('edulevel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oopk.edulevelprogram', verbose_name='Приемная кампания')),
            ],
            options={
                'verbose_name': 'Экзамены',
                'verbose_name_plural': 'Экзамены',
            },
        ),
    ]
