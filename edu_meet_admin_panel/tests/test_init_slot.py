from django.test import TestCase
from edu_meet_admin_panel.models import Slot, User
from django.core.management import call_command


class InitSlotsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Временно включаем `managed = True`
        Slot._meta.managed = True
        User._meta.managed = True

        # Применяем миграции, чтобы создать все таблицы
        call_command('migrate', run_syncdb=True, verbosity=0)

        # Загружаем фикстуры
        call_command("loaddata", "users.json")

    @classmethod
    def tearDownClass(cls):
        # Возвращаем `managed = False`, чтобы не затронуть реальную базу
        Slot._meta.managed = False
        User._meta.managed = False
        super().tearDownClass()

    def test_slots_generation(self):
        # Проверяем начальное состояние
        self.assertEqual(Slot.objects.count(), 0)

        # Запускаем команду init_slots
        call_command('init_slots')

        # Проверяем, что добавлены новые слоты
        self.assertGreater(Slot.objects.count(), 1)
        self.assertEqual(Slot.objects.count(), 120)
