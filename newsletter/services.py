import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from config.settings import CASHE_ENABLED
from newsletter.models import Newsletter, Message, MailingAttempt
from apscheduler.schedulers.background import BackgroundScheduler


def send_newsletter(newsletter):
    """Функция отправки рассылки и записи попыток"""
    try:
        message_instance = newsletter.message
        server_response = send_mail(
            subject=message_instance.letter_theme,
            message=message_instance.letter_body,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in newsletter.client.all()],
            fail_silently=False,
        )
        attempt = MailingAttempt.objects.create(newsletter=newsletter, server_response=server_response)
        if server_response:
            attempt.status = 'Успешно'
            attempt.save()
        if newsletter.status == 'CREATED':
            newsletter.status = 'STARTED'
            newsletter.save()
    except smtplib.SMTPException as e:
        attempt = MailingAttempt.objects.create(newsletter=newsletter, server_response=e)
        attempt.status = 'Неуспешно'
        attempt.save()
    print(attempt.status)


def send_periodic_newsletter():
    """Функция периодической отправки рассылки
    Фильтрует все рассылки по дате начала и конца и отправляет в нужный момент"""
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    for newsletter in Newsletter.objects.all():
        if newsletter.start_time < current_datetime < newsletter.end_time:
            attempt = MailingAttempt.objects.filter(newsletter=newsletter)
            print(attempt)
            # Если рассылка старая и попытки уже были то:
            if attempt.exists():
                # Достать последнюю попытку, чтобы сравнить ее время с текущим временем:
                last_attempt = attempt.order_by('date_time').last()
                current_timedelta = current_datetime - last_attempt.date_time
            else:  # Если же рассылка совершенно новая, то сравниваем текущее время со стартом отправки рассылки
                current_timedelta = current_datetime - newsletter.start_time

            # Проверка на периодичность рассылки:
            if newsletter.periodicity == 'MINUTLY' and current_timedelta >= timedelta(minutes=1):
                send_newsletter(newsletter)
                print(f'Выполнена рассылка раз в минуту, время: {datetime.now(zone)}')
            elif newsletter.periodicity == 'DAILY' and current_timedelta >= timedelta(days=1):
                send_newsletter(newsletter)
                print(f'Выполнена рассылка раз в день, время: {datetime.now(zone)}')
            elif newsletter.periodicity == 'WEEKLY' and current_timedelta >= timedelta(weeks=1):
                send_newsletter(newsletter)
                print(f'Выполнена рассылка раз в неделю, время: {datetime.now(zone)}')
            elif newsletter.periodicity == 'MONTHLY' and current_timedelta >= timedelta(weeks=4):
                send_newsletter(newsletter)
                print(f'Выполнена рассылка раз в месяц, время: {datetime.now(zone)}')

        elif current_datetime > newsletter.end_time:
            newsletter.status = 'FINISHED'
            newsletter.save()


def start_sheduler():
    scheduler = BackgroundScheduler()
    if not scheduler.get_jobs():
        scheduler.add_job(send_periodic_newsletter, 'interval', seconds=10)
    if not scheduler.running:
        scheduler.start()


def get_newsletter_from_cashe(obj):
    """Если есть в кеше -> берем оттуда, если нет -> кладем в кеш"""
    if not CASHE_ENABLED:
        print(obj)
        return obj
    key = "newsletter_list"
    objects = cache.get(key)
    if objects is not None:
        return objects
    objects = obj
    cache.set(key, objects)
    return objects