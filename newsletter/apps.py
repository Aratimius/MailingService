from time import sleep

from django.apps import AppConfig


class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'

#  РАСКОММЕНТИРОВАТЬ КОД ДЛЯ АВТОМАТИЗАЦИИ ОТПРАВКИ РАССЫЛОК -> ЗАПУСТИТЬ СЕРВЕР
    def ready(self):
        from newsletter.services import start_sheduler
        sleep(2)
        start_sheduler()
