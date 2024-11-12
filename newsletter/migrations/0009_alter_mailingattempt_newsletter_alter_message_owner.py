# Generated by Django 4.2.2 on 2024-11-10 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newsletter', '0008_alter_message_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingattempt',
            name='newsletter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='newsletter.newsletter', verbose_name='попытка рассылки'),
        ),
        migrations.AlterField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
