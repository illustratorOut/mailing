from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helper.models import Mailing
from helper.tasks import schedule_send


class MailingAPIView(APIView):
    """Создание рассылки"""

    def post(self, request):
        data = request.data

        delay = data.get('delay')
        recipients = data.get('recepient') if isinstance(data.get('recepient'), list) else [data.get('recepient')]

        if data.get('recepient') and data.get('message'):

            for recepient in recipients:
                message_type = 'telegram' if str(recepient).isdigit() else 'email'

                message = Mailing(
                    message=data.get('message'),
                    recepient=recepient,
                    delay=delay,
                    message_type=message_type,
                )
                message.save()
                schedule_send.delay(message.id, delay)

            return Response({"status": "Сообщения добавлены в очередь"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"status": "Не валидный запрос"}, status=status.HTTP_400_BAD_REQUEST)
