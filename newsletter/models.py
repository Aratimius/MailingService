from datetime import datetime

from django.db import models

from users.models import User


class Client(models.Model):
    """Модель клиента, которому будет отправлена рассылка"""
    email = models.CharField(max_length=100, verbose_name='email', help_text='введите email')
    name_surname = models.CharField(max_length=200, verbose_name='Ф.И.О', help_text='введите Ф.И.О.')
    comment = models.TextField(verbose_name='комментарий', blank=True, null=True)

    owner = models.ForeignKey(User, verbose_name='пользователь', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.name_surname}: {self.email}'


class Message(models.Model):
    """Модель сообщения для рассылки"""
    letter_theme = models.CharField(max_length=200, verbose_name='тема письма', help_text='напишите тему письма')
    letter_body = models.TextField(verbose_name='тело письма', help_text='вводите текст письма здесь', blank=True,
                                   null=True)
    owner = models.ForeignKey(User, verbose_name='пользователь', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'

    def __str__(self):
        return self.letter_theme


class Newsletter(models.Model):
    """Модель рассылки"""
    CREATED = 'Создана'
    STARTED = 'Запущена'
    FINISHED = 'Завершена'
    MINUTLY = 'minutly'
    DAILY = 'daily',
    WEEKLY = 'weekly',
    MONTHLY = 'monthly',

    STATUS_CHOICES = (
        ('CREATED', 'Создана'),
        ('STARTED', 'Запущена'),
        ('FINISHED', 'Завершена'),
    )

    FREQUENCY_CHOICES = (
        ('MINUTLY', 'раз в минуту'),
        ('DAILY', 'раз в день'),
        ('WEEKLY', 'раз в неделю'),
        ('MONTHLY', 'раз в месяц'),
    )
    start_time = models.DateTimeField(default=datetime.now, verbose_name='дата начала')
    end_time = models.DateTimeField(verbose_name='дата окончания', blank=True, null=True)
    periodicity = models.CharField(max_length=150, verbose_name='периодичность', choices=FREQUENCY_CHOICES,
                                   default=DAILY)
    status = models.CharField(max_length=150, verbose_name='статус рассылки', choices=STATUS_CHOICES, default=CREATED)

    client = models.ManyToManyField(Client, verbose_name='клиент',
                                    help_text='необходимо выбрать хотя бы одного клиента')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, primary_key=True, verbose_name='сообщение',
                                   help_text='обязательное поле')
    owner = models.ForeignKey(User, verbose_name='пользователь', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [('can_change_status', 'can change newsletter status'),  # Менять статус рассылки(отключать)
                       ('can_view_newsletters', 'can view newsletters')  # Посматривать список рассылок
                       ]


    def __str__(self):
        return f'{self.message}'


class MailingAttempt(models.Model):
    LOG_SUCCESS = 'Успешно'
    LOG_FAIL = 'Неуспешно'

    STATUS_VARIANTS = [
        (LOG_SUCCESS, 'Успешно'),
        (LOG_FAIL, 'Неуспешно'),
    ]
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=150, verbose_name='статус попытки', choices=STATUS_VARIANTS)
    server_response = models.CharField(max_length=150, verbose_name='ответ постового сервера')
    newsletter = models.ForeignKey(Newsletter, on_delete=models.SET_NULL, verbose_name='попытка рассылки', null=True)

    class Meta:
        verbose_name = 'попытка'
        verbose_name_plural = 'попытки'
