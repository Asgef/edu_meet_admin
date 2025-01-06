from django.test import TestCase
from django.core.management import call_command
from edu_meet_admin_panel.models import Slot, User
from django.utils.timezone import now


class DeleteUnusedSlotsFixtureTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Временно включаем `managed = True`
        Slot._meta.managed = True
        User._meta.managed = True

        call_command('migrate', run_syncdb=True, verbosity=0)

        call_command(
            'loaddata', 'last_slots.json', 'users.json'
        )

    @classmethod
    def tearDownClass(cls):
        Slot._meta.managed = False
        User._meta.managed = False
        super().tearDownClass()

    def test_delete_past_unused_slots_with_fixture(self):
        # Подсчитываем общее количество слотов до удаления
        initial_count = Slot.objects.count()

        # Подсчитываем количество слотов, которые должны быть удалены
        expected_to_delete = Slot.objects.filter(
            date__lt=now().date(),
            status__in=['available', 'unavailable']
        ).count()

        # Запускаем команду
        call_command('delete_unused_slots')

        # Подсчитываем оставшиеся слоты
        remaining_slots = Slot.objects.count()
        deleted_slots = initial_count - remaining_slots

        # Утверждаем, что удалено ожидаемое количество записей
        self.assertEqual(deleted_slots, expected_to_delete)

        # Утверждаем, что больше нет слотов, которые должны были быть удалены
        self.assertEqual(Slot.objects.filter(
            date__lt=now().date(),
            status__in=['available', 'unavailable']
        ).count(), 0)
