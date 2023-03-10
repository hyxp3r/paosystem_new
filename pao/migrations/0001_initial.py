# Generated by Django 4.1.2 on 2022-12-29 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fioExpert', models.CharField(max_length=50)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pao.department')),
            ],
        ),
        migrations.CreateModel(
            name='ContractNames',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sectionEC', models.CharField(max_length=5)),
                ('descriptionEC', models.TextField()),
                ('expertEC', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pao.expert')),
            ],
        ),
        migrations.CreateModel(
            name='CheckEc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onReview', models.IntegerField()),
                ('verified', models.IntegerField()),
                ('contractName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pao.contractnames')),
            ],
        ),
    ]
