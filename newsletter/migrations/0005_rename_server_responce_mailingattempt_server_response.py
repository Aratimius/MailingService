# Generated by Django 5.1.2 on 2024-11-08 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0004_remove_newsletter_date_time_newsletter_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mailingattempt',
            old_name='server_responce',
            new_name='server_response',
        ),
    ]