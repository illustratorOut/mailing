from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Mailing, JournalLogs
from .services import send_message_telegram


@shared_task(bind=True)
def send_email(self, message_id):
    try:
        message = Mailing.objects.get(id=message_id)

        if message.type == 'email':
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

        log = JournalLogs(message=message, status=True)
        log.save()
    except Exception as e:
        message = Mailing.objects.get(id=message_id)
        log = JournalLogs(message=message, status=False, message_error=str(e))
        log.save()
        raise self.retry(exc=e, countdown=60 * 5)  # Повторная попытка через 5 минут


@shared_task(bind=True)
def schedule_send(self, message_id, delay):
    if str(delay) == '0':
        return send_email.delay(message_id)
    if str(delay) == '1':
        eta = now() + timedelta(hours=1)
    elif str(delay) == '2':
        eta = now() + timedelta(days=1)

    return send_email.apply_async((message_id,), eta=eta)
