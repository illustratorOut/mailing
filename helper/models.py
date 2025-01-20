from django.db import models

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
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, verbose_name='Тип сообщения')
    delay = models.PositiveSmallIntegerField(verbose_name='Периодичность')
    shipping = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Содержимое сообщения - {self.message}, получатель: {self.recepient}'

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id})'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class JournalLogs(models.Model):
    message = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    message_error = models.TextField(verbose_name='Сообщение об ошибке')
    is_error = models.BooleanField(verbose_name='Является ошибкой')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Логирование: "{self.message}"'

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'
