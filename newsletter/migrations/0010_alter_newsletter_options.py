# Generated by Django 4.2.2 on 2024-11-11 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0009_alter_mailingattempt_newsletter_alter_message_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'permissions': [('can_change_status', 'can change newsletter status')], 'verbose_name': 'рассылка', 'verbose_name_plural': 'рассылки'},
        ),
    ]