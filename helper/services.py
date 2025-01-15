import os
import requests


def send_message_telegram(chat_id, message_text):
    token = os.getenv('TELEGRAM_TOKEN')

    if not token:
        raise ValueError("Токен Telegram-бота не задан в переменных окружения")

    response = requests.post(
        url=f'https://api.telegram.org/bot{token}/sendMessage',
        json={
            'chat_id': int(chat_id),
            'text': str(message_text),
        }
    )
    if response.status_code != 200:
        raise ValueError(response.json().get('description'))
    return response.status_code
