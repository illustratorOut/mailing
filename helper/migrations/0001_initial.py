# Generated by Django 5.1.4 on 2025-01-14 20:48

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1024, verbose_name='Сообщения')),
                ('recepient', models.CharField(max_length=150, verbose_name='Получатель')),
                ('delay', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Периодичность')),
                ('release_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='JournalLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logs', models.TextField(verbose_name='Логирование')),
                ('release_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='helper.mailing')),
            ],
            options={
                'verbose_name': 'Лог',
                'verbose_name_plural': 'Логи',
            },
        ),
    ]
