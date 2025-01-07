from django.core.management.base import BaseCommand
from django.utils.timezone import now
from edu_meet_admin_panel.models import Slot


class Command(BaseCommand):
    help = 'Delete unused and past slots'

    def handle(self, *args, **kwargs):
        # Текущая дата и время
        current_datetime = now()

        # Фильтруем слоты с прошедшей датой и статусами
        # 'available' или 'unavailable'
        slots_to_delete = Slot.objects.filter(
            date__lt=current_datetime.date(),
            status__in=['available', 'unavailable']
        ).exclude(order__isnull=False)

        # Сохраняем количество удаленных записей
        deleted_count, _ = slots_to_delete.delete()

        # Вывод результата
        self.stdout.write(
            self.style.SUCCESS(f'{deleted_count} unused slots deleted')
        )
