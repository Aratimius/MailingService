# Generated by Django 4.2.2 on 2024-11-10 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='token',
        ),
    ]
