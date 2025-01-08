from edu_meet_admin_panel.models import Order, User, Slot, AcademicSubject


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
            self.slot.status = 'accepted'
        if self.status == 'canceled':
            self.slot.status = 'accepted'
        if self.status == 'pending':
            self.slot.status = 'pending'
        self.slot.save()

    def save(self, *args, **kwargs):
        self.update_slot_status()
        super().save(*args, **kwargs)


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
