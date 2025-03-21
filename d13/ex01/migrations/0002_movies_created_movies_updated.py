# Generated by Django 4.2.19 on 2025-03-21 09:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ex01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movies',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='movies',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
