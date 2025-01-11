from django.contrib import admin
from edu_meet_admin_panel.admin_panel.slot_admin import SlotChoiceField
from edu_meet_admin_panel.admin_panel.user_admin import UserChoiceField
from edu_meet_admin_panel.models import User, AcademicSubject
from edu_meet_admin_panel.models import Slot
from django import forms
from edu_meet_admin_panel.admin_panel.subject_admin import SubjectChoiceField
from edu_meet_admin_panel.admin_panel.filters import (
    CustomDateFilter, FutureWeeksFilter, SpecificDateFilter,
    CustomStatusFilterOrder
)
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from django.conf import settings
from edu_meet_admin_panel.proxy_models import OrderProxy


class OrderAdminForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('accepted', 'Принят'),
        ('declined', 'Отклонен'),
        ('canceled', 'Закрыт'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")

    tutor = UserChoiceField(
        queryset=User.objects.all(),
        label="Репетитор"
    )
    student = UserChoiceField(
        queryset=User.objects.all(),
        label="Ученик",
        required=False
    )
    subject = SubjectChoiceField(
        queryset=AcademicSubject.objects.all(),
        label="Предмет"
    )
    slot = SlotChoiceField(
        queryset=Slot.objects.all(),
        label="Слот"
    )
    comment = forms.CharField(
        widget=forms.Textarea,
        label="Комментарий",
        required=False
    )

    class Meta:
        model = OrderProxy
        fields = '__all__'
        labels = {
            'date': 'Дата',
            'created_at': 'Дата создания',
            'updated_at': 'Последнее обновление',
            'slot': 'Слот',
            'comment': 'Комментарий',
            'status': 'Статус',
            'subject': 'Предмет',
            'tutor': 'Репетитор',
            'student': 'Ученик',
        }


class OrderAdmin(admin.ModelAdmin):
    actions = [
        'set_status_accepted', 'set_status_declined', 'set_status_canceled'
    ]
    form = OrderAdminForm
    list_display = (
        'id', 'student_col', 'tutor_col', 'slot_col', 'subject_col',
        'status_col', 'date_col', 'comment_col'
    )
    search_fields = ('student__username', 'tutor__username', 'comment')
    list_filter = (
        CustomStatusFilterOrder, CustomDateFilter, FutureWeeksFilter,
        SpecificDateFilter
    )
    readonly_fields = ['slot_link', 'subject_link', 'student_link']

    def student_link(self, obj):
        if obj and obj.student:
            # Генерация ссылки на объект User в вашей модели
            url = reverse('admin:edu_meet_admin_panel_userproxy_change',
                          args=[obj.student.id])
            return format_html(
                '<a href="{}" target="_blank">Перейти к ученику</a>', url)
        return "Нет данных"

    student_link.short_description = "Ученик"

    def slot_link(self, obj):
        if obj and obj.slot:
            # Генерация ссылки на объект Slot
            url = reverse('admin:edu_meet_admin_panel_slotproxy_change',
                          args=[obj.slot.id])
            return format_html(
                '<a href="{}" target="_blank">Перейти к слоту</a>', url)
        return "Нет данных"

    slot_link.short_description = "Слот"

    def subject_link(self, obj):
        if obj and obj.subject:
            # Генерация ссылки на объект AcademicSubject
            url = reverse(
                'admin:edu_meet_admin_panel_academicsubjectproxy_change',
                args=[obj.subject.id])
            return format_html(
                '<a href="{}" target="_blank">Перейти к предмету</a>', url)
        return "Нет данных"

    subject_link.short_description = "Предмет"

    def student_col(self, obj):
        return obj.student.username if obj.student else "Не назначен"
    student_col.short_description = "Ученик"
    student_col.admin_order_field = 'student__username'

    def tutor_col(self, obj):
        return obj.tutor.username if obj.tutor else "Не назначен"
    tutor_col.short_description = "Репетитор"
    tutor_col.admin_order_field = 'tutor__username'

    def slot_col(self, obj):
        return (
            f"{obj.slot.id} {obj.slot.date} "
            f"{obj.slot.time_start.strftime('%H:%M')}"
        ) if obj.slot else "Нет слота"
    slot_col.short_description = "Слот"
    slot_col.admin_order_field = 'slot__id'

    def subject_col(self, obj):
        return obj.subject.name if obj.subject else "Без предмета"
    subject_col.short_description = "Предмет"
    subject_col.admin_order_field = 'subject__name'

    def status_col(self, obj):
        choices = {
            'pending': 'Ожидает подтверждения',
            'accepted': 'Принят',
            'declined': 'Отклонен',
            'canceled': 'Закрыт',
        }
        return choices.get(obj.status, obj.status)
    status_col.short_description = "Статус"
    status_col.admin_order_field = 'status'

    def date_col(self, obj):
        return obj.date.strftime("%d.%m.%Y %H:%M")
    date_col.short_description = "Дата"
    date_col.admin_order_field = 'date'

    def comment_col(self, obj):
        return obj.comment if obj.comment else "Нет комментария"
    comment_col.short_description = "Комментарий"
    comment_col.admin_order_field = 'comment'

    def set_status_accepted(self, request, queryset):
        updated = queryset.update(status='accepted')
        OrderProxy.bulk_update_slot_statuses(
            queryset.values_list('id', flat=True)
        )
        # TODO: При масштабировании проекта следует пересмотреть отправку массовых уведомлений.
        for order in queryset:
            order.notify_user()
        self.message_user(
            request,
            f"{updated} заявок отмечены как 'Принят'",
            messages.SUCCESS
        )
    set_status_accepted.short_description = "Отметить как 'Принят'"

    def set_status_declined(self, request, queryset):
        OrderProxy.bulk_update_slot_statuses(
            queryset.values_list('id', flat=True)
        )
        updated = queryset.update(status='declined')
        for order in queryset:
            order.notify_user()
        self.message_user(
            request,
            f"{updated} заявок отмечены как 'Отклонен'",
            messages.SUCCESS
        )
    set_status_declined.short_description = "Отметить как 'Отклонен'"

    def set_status_canceled(self, request, queryset):
        updated = queryset.update(status='canceled')
        OrderProxy.bulk_update_slot_statuses(
            queryset.values_list('id', flat=True)
        )
        for order in queryset:
            order.notify_user()
        self.message_user(
            request,
            f"{updated} заявок отмечены как 'Закрыт'",
            messages.SUCCESS
        )
    set_status_canceled.short_description = "Отметить как 'Закрыт'"

    # Установим репетитора по умолчанию в форме
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        default_tutor_id = User.objects.get(tg_id=settings.TUTOR_TG_ID).id
        if not obj:
            form.base_fields['tutor'].initial = default_tutor_id

        return form


__all__ = ['OrderAdmin']
