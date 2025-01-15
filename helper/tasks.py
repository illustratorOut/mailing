from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now

from .models import Mailing, JournalLogs


@shared_task(bind=True)
def send_email(self, message_id):
    try:
        message = Mailing.objects.get(id=message_id)

        if message.type == 'email':
            print(message)
            print(message.recepient)
            send_mail(
                subject="Уведомление",
                message=message.message,
                from_email="bmgula55@mail.ru",
                recipient_list=[message.recepient],
                fail_silently=False,
            )
        else:
            print(f"Отправлено сообщение в Telegram: {message.message}")

        log = JournalLogs(message=message, status=True)
        log.save()
    except Exception as e:
        log = JournalLogs(message=message, status=False, logs=str(e))
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
