from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/photo', blank=True, null=True, verbose_name='изображение')
    creation_date = models.DateField(blank=True, null=True, verbose_name='дата публикации', auto_now_add=True)
    publication_sign = models.BooleanField(default=False, verbose_name='опубликовано')
    views = models.IntegerField(default=0, verbose_name='колличество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'