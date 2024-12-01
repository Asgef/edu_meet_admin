from django.core.management.base import BaseCommand
from django.utils.timezone import now, make_aware, timedelta  # Работа с временными зонами и временными интервалами
from datetime import datetime, time  # Работа с датами и временем
from edu_meet_admin_panel.models import Slot, User  # Модели вашего приложения

class Command(BaseCommand):
    help = 'Initialize slots'

    def add_arguments(self, parser):
        # Добавление опционального аргумента для указания количества недель
        parser.add_argument(
            '--weeks',
            type=int,
            default=4,  # По умолчанию 4 недели
            help='Количество недель для генерации слотов (по умолчанию 4)'
        )

    def handle(self, *args, **kwargs):
        weeks = kwargs['weeks']  # Получаем значение аргумента --weeks
        # Выбираем первого администратора как репетитора
        tutor = User.objects.filter(is_admin=True).first()

        # Проверяем, есть ли администратор, если нет — выводим ошибку
        if not tutor:
            self.stdout.write(self.style.ERROR('Нет доступного администратора для назначения слотов.'))
            return

        # Устанавливаем начальную и конечную дату
        start_date = now().date()  # Сегодняшняя дата
        end_date = start_date + timedelta(weeks=weeks)  # Дата через указанное количество недель

        # Пример расписания для одного дня (время начала и окончания слотов)
        daily_slots = [
            (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0)),
            (time(14, 0), time(15, 0)),
            (time(15, 0), time(16, 0)),
            (time(17, 0), time(18, 0)),
        ]

        created_slots = 0  # Счетчик для созданных слотов

        # Генерация слотов по дням в заданном диапазоне
        for single_date in (start_date + timedelta(days=n) for n in range((end_date - start_date).days)):
            # Пропускаем выходные (суббота и воскресенье)
            if single_date.weekday() in [5, 6]:  # 5 = суббота, 6 = воскресенье
                continue

            # Преобразуем "наивную" дату в "осведомленную" с временной зоной
            single_date_aware = make_aware(datetime.combine(single_date, time.min))

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
