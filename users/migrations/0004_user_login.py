# Generated by Django 4.2.2 on 2024-11-10 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login',
            field=models.BooleanField(default=True),
        ),
    ]
