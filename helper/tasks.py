from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from .models import Mailing, JournalLogs
from .services import send_message_telegram, send_message_email


@shared_task(bind=True)
def send_message(self, message_id):
    """Отправка сообщений"""
    message = Mailing.objects.get(id=message_id)

    try:
        if message.message_type == 'email':
            send_message_email(message.recepient, message.message)
        elif message.message_type == 'telegram':
            send_message_telegram(message.recepient, message.message)

        log = JournalLogs(message=message, is_error=False)
        log.save()
    except Exception as e:
        log = JournalLogs(message=message, is_error=True, message_error=str(e))
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
