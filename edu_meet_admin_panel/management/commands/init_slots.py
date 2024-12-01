from django.core.management.base import BaseCommand
from django.utils.timezone import now, make_aware, timedelta
from datetime import datetime, time
from edu_meet_admin_panel.models import Slot, User
from django.conf import settings


class Command(BaseCommand):
    help = 'Initialize slots'

    def add_arguments(self, parser):
        # Добавление опционального аргумента для указания количества недель
        parser.add_argument(
            '--weeks',
            type=int,
            default=4,  # По умолчанию 4 недели
            help='Number of weeks to generate slots (default 4)'
        )

    def handle(self, *args, **kwargs):
        weeks = kwargs['weeks']  # Получаем значение аргумента --weeks
        # Выбираем первого администратора как репетитора
        tutor = User.objects.filter(
            tg_id=settings.SLOT_SETTINGS['TUTOR_TG_ID']
        ).first()

        # Проверяем, есть ли администратор, если нет — выводим ошибку
        if not tutor:
            self.stdout.write(self.style.ERROR(
                'There is no administrator available to assign slots.')
            )
            return

        # Устанавливаем начальную и конечную дату
        start_date = now().date()  # Сегодняшняя дата
        # Дата через указанное количество недель
        end_date = start_date + timedelta(weeks=weeks)

        # Пример расписания для одного дня (время начала и окончания слотов)
        daily_slots = settings.SLOT_SETTINGS['DAILY_SLOTS']

        created_slots = 0  # Счетчик для созданных слотов

        # Генерация слотов по дням в заданном диапазоне
        for single_date in (start_date + timedelta(days=n)
                            for n in range((end_date - start_date).days)):
            # Пропускаем выходные (суббота и воскресенье)
            if single_date.weekday() in settings.SLOT_SETTINGS['WEEKEND']:
                continue

            # Преобразуем "наивную" дату в "осведомленную" с временной зоной
            single_date_aware = make_aware(
                datetime.combine(single_date, time.min)
            )

            # Генерация слотов для текущей даты
            for start_time, end_time in daily_slots:
                # Проверяем, есть ли уже слот с такими параметрами
                slot, created = Slot.objects.get_or_create(
                    date=single_date_aware,  # Дата слота
                    time_start=start_time,  # Время начала
                    time_end=end_time,  # Время окончания
                    tutor=tutor,  # Репетитор
                    defaults={  # Значения по умолчанию
                        'status': 'available',  # Слот доступен
                        'comment': '',  # Комментарий пустой
                    }
                )
                if created:
                    created_slots += 1  # Увеличиваем счетчик созданных слотов

        # Выводим результат выполнения команды
        self.stdout.write(
            self.style.SUCCESS(f'{created_slots} new slots created')
        )
