from edu_meet_admin_panel.models import Order, User, Slot, AcademicSubject
from django.conf import settings
import requests
import logging


logger = logging.getLogger('django')



class OrderProxy(Order):
    class Meta:
        proxy = True
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        student_name = self.student.username \
            if self.student else "Неизвестный ученик"
        date_time = (f"{self.date.strftime("%d.%m.%Y")} "
                     f"{self.slot.time_start.strftime('%H:%M')}")
        return f"Заказ {self.id}: {student_name} -> {date_time}"

    def update_slot_status(self):
        if self.status == 'accepted':
            self.slot.status = 'accepted'
        if self.status == 'declined':
            self.slot.status = 'available'
        if self.status == 'canceled':
            self.slot.status = 'accepted'
        if self.status == 'pending':
            self.slot.status = 'pending'
        self.slot.save()

    @staticmethod
    def bulk_update_slot_statuses(order_ids):
        orders = OrderProxy.objects.filter(id__in=order_ids).select_related(
            'slot')
        for order in orders:
            if order.status == 'accepted':
                order.slot.status = 'accepted'
            elif order.status == 'declined':
                order.slot.status = 'available'
            elif order.status == 'canceled':
                order.slot.status = 'accepted'
            elif order.status == 'pending':
                order.slot.status = 'pending'
            order.slot.save()

    def notify_user(self):
        # TODO: Реализовать защиту с использованием auth токена.
        if self.student and self.student.tg_id:
            webhook_url = settings.TELEGRAM_BOT_WEBHOOK_URL
            payload = {
                "tg_id": self.student.tg_id,
                "message": f"Статус вашего заказа от "
                           f"{self.date.strftime('%d.%m.%Y')} "
                           f"{self.slot.time_start.strftime('%H:%M')} "
                           f"изменена на {self.status}"
            }
            try:
                logger.info(f'>>>>>>>>>>>>>>> {payload}')
                response = requests.post(webhook_url, json=payload)
                logger.info(f'>>>>>>>>>>>>>>> {response.text}')
                response.raise_for_status()
            except requests.RequestException as e:
                logger.error(f"Error sending Telegram notification: {e}")

    def save(self, *args, **kwargs):
        self.update_slot_status()
        super().save(*args, **kwargs)
        self.notify_user() # Уведомить пользователя о смене статуса


class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    # Переопределяем verbose_name для полей
    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


class SlotProxy(Slot):
    class Meta:
        proxy = True
        verbose_name = "Слот"
        verbose_name_plural = "Слоты"

    def __str__(self):
        return (
            f"Слот {self.id} ({self.date} "
            f"{self.time_start.strftime('%H:%M')} - "
            f"{self.time_end.strftime('%H:%M')})"
        )


class AcademicSubjectProxy(AcademicSubject):
    class Meta:
        proxy = True
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name
