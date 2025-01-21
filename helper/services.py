import os
import requests
from django.core.mail import send_mail


def send_message_telegram(chat_id: int, message_text: str):
    """Отправка сообщений в Telegram"""
    token = os.getenv('TELEGRAM_TOKEN')

    if not token:
        raise ValueError("Токен Telegram-бота не задан в переменных окружения")

    try:
        response = requests.post(
            url=f'https://api.telegram.org/bot{token}/sendMessage',
            json={
                'chat_id': int(chat_id),
                'text': str(message_text),
            }
        )

        if response.status_code == 200:
            print(f"В Telegram chat_id = {chat_id} отправлено сообщение ('{message_text}')")
        else:
            raise ValueError(response.json().get('description'))

        return response.status_code
    except Exception as e:
        raise ValueError(e)


def send_message_email(recepient: str, message_text: str):
    """Отправка сообщений на Email"""
    email = os.getenv('EMAIL_HOST_USER')

    if not email:
        raise ValueError("EMAIL_HOST_USER не задан в переменных окружения")

    try:
        send_mail(
            subject="Уведомление",
            message=message_text,
            from_email=email,
            recipient_list=[recepient],
            fail_silently=False,
        )
        print(f"На почту email = {recepient} отправлено сообщение ('{message_text}')")
    except Exception as e:
        raise ValueError(e)
