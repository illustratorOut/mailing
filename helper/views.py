from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from helper.models import Mailing
from .tasks import schedule_send


class MailingAPIView(APIView):
    '''Создание рассылки'''

    def post(self, request):
        data = request.data
        messages = []

        recipients = data.get('recepient') if isinstance(data.get('recepient'), list) else [data.get('recepient')]

        if data.get('recepient') and data.get('message'):

            for recepient in recipients:
                if str(recepient).isdigit():
                    message_type = 'telegram'
                else:
                    message_type = 'email'

                message = Mailing(
                    message=data.get('message'),
                    recepient=recepient,
                    delay=data.get('delay'),
                    type=message_type,
                )
                message.save()
                messages.append(message.id)

            for message_id in messages:
                schedule_send.delay(message_id, data.get('delay'))

            return Response({"status": "Сообщения поставлены в очередь"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"status": "Не валидный запрос"}, status=status.HTTP_400_BAD_REQUEST)
