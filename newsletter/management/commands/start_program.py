import smtplib
from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.core.mail import send_mail

from newsletter.models import Newsletter, Message, MailingAttempt
from django.core.management import BaseCommand

from newsletter.services import send_newsletter, send_periodic_newsletter


class Command(BaseCommand):
    """Команда для автоматизации рассылки"""

    def handle(self, *args, **options):
        send_periodic_newsletter()
