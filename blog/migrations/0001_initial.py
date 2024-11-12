# Generated by Django 4.2.2 on 2024-11-11 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='заголовок')),
                ('content', models.TextField(verbose_name='содержимое')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='blog/photo', verbose_name='изображение')),
                ('creation_date', models.DateField(auto_now_add=True, null=True, verbose_name='дата публикации')),
                ('publication_sign', models.BooleanField(default=False, verbose_name='опубликовано')),
                ('views', models.IntegerField(default=0, verbose_name='колличество просмотров')),
            ],
            options={
                'verbose_name': 'запись',
                'verbose_name_plural': 'записи',
            },
        ),
    ]
