<H1> Шаблон файла .env</H1>

```text 
POSTGRES_DB=
POSTGRES_PASSWORD=
POSTGRES_USER=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=
TELEGRAM_TOKEN=

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

CELERY_BROKER_URL=redis://redis:6379
CELERY_RESULT_BACKEND=redis://redis:6379
 ```

## Перечень реализованных требований

| Task                                                                        | Status |
|-----------------------------------------------------------------------------|--------|
| Сервис должен иметь одну точку входа: /api/notify/                          | ✅      |
| Параметр recepient может содержать одного получателя или список получателей | ✅      |
| Параметр delay отвечает за задержку отправки                                | ✅      |
| При получении сообщение должно складываться в отдельную таблицу             | ✅      |
| А при рассылке необходимо записывать лог о попытке отправки в БД            | ✅      |
| Сама отправка должна осуществляться с помощью очереди через celery          | ✅      |
| Проект должен быть оформлен согласно PEP8                                   | ✅      |

