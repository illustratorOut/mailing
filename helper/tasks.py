from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Mailing, JournalLogs
from .services import send_message_telegram


@shared_task(bind=True)
def send_message(self, message_id):
    """ Отправка сообщений """
    try:
        message = Mailing.objects.get(id=message_id)

        if message.message_type == 'email':
            send_mail(
                subject="Уведомление",
                message=message.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[message.recepient],
                fail_silently=False,
            )
            print(f"Отправлено сообщение ({message.message}) на почту: {message.recepient}")
        else:
            status_code = send_message_telegram(message.recepient, message.message)
            if status_code == 200:
                print(f"Отправлено сообщение ({message.message}) в Telegram: {message.recepient}")

        log = JournalLogs(message=message, is_error=True)
        log.save()
    except Exception as e:
        message = Mailing.objects.get(id=message_id)
        log = JournalLogs(message=message, is_error=False, message_error=str(e))
        log.save()


@shared_task(bind=True)
def schedule_send(self, message_id: int, delay: int):
    """Отправка сообщений с задержкой"""
    delay = str(delay)

    if delay == '0':
        return send_message.delay(message_id)
    elif delay == '1':
        eta = now() + timedelta(hours=1)
    elif delay == '2':
        eta = now() + timedelta(days=1)
    else:
        return
    return send_message.apply_async((message_id,), eta=eta)
