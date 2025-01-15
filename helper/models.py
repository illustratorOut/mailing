from django.db import models
from django.utils import timezone

NULLABLE = {
    'blank': True,
    'null': True
}


class Mailing(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ('email', 'Email'),
        ('telegram', 'Telegram'),
    )

    message = models.CharField(max_length=1024, verbose_name='Сообщения')
    recepient = models.CharField(max_length=150, verbose_name='Получатель')
    type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, verbose_name='Принадлежность получателя')
    delay = models.PositiveSmallIntegerField(default=0, verbose_name='Периодичность', **NULLABLE)
    release_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return f'Содержимое сообщения - {self.message}, получатель: {self.recepient}'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class JournalLogs(models.Model):
    message = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    message_error = models.TextField(verbose_name='Сообщение об ошибке')
    status = models.BooleanField(verbose_name='Статус')
    release_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    def __str__(self):
        return f'Логирование: "{self.logs}"'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
