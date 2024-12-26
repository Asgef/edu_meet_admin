from django.contrib import admin
from edu_meet_admin_panel.admin_panel.user_admin import UserChoiceField
from edu_meet_admin_panel.models import Slot
from edu_meet_admin_panel.proxy_models import UserProxy
from django import forms
from edu_meet_admin_panel.admin_panel.filters.slots import *


# Выпадающий список для статуса
class SlotAdminForm(forms.ModelForm):
    # корректируем поле статуса
    STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('pending', 'Ожидает подтверждения'),
        ('accepted', 'Принят'),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")

    tutor = UserChoiceField(
        queryset=UserProxy.objects.all(),
        label="Репетитор"
    )
    student = UserChoiceField(
        queryset=UserProxy.objects.all(),
        label="Ученик",
        required=False
    )
    comment= forms.CharField(
        widget=forms.Textarea,
        label="Комментарий",
        required=False
    )
    class Meta:
        model = Slot
        fields = '__all__'
        labels = {
            'date': 'Дата',
            'time_start': 'Начало времени',
            'time_end': 'Конец времени',
            'tutor': 'Репетитор',
            'student': 'Ученик',
            'comment': 'Комментарий'
        }

class SlotAdmin(admin.ModelAdmin):
    form = SlotAdminForm
    list_display = (
        'id', 'status_col', 'slot_col','date_col', 'time_start_col',
        'time_end_col', 'tutor_col', 'student_col', 'comment_col'
    )
    search_fields = ('tutor__username', 'student__username', 'comment')
    list_filter = (
        CustomStatusFilter, CustomDateFilter, HourStartFilter,
        FutureWeeksFilter, SpecificDateFilter
    )

    def slot_col(self, obj):
        return f"{str(obj.date)} {str(obj.time_start.strftime('%H:%M'))}"
    slot_col.short_description = "Слот"

    def date_col(self, obj):
        return obj.date.strftime("%d.%m.%Y")
    date_col.short_description = "Дата"
    date_col.admin_order_field = 'date'

    def time_start_col(self, obj):
        return obj.time_start.strftime("%H:%M")
    time_start_col.short_description = "Начало времени"
    time_start_col.admin_order_field = 'time_start'

    def time_end_col(self, obj):
        return obj.time_end.strftime("%H:%M")
    time_end_col.short_description = "Конец времени"
    time_end_col.admin_order_field = 'time_end'

    def tutor_col(self, obj):
        if obj.tutor:
            return f"{obj.tutor.first_name} {obj.tutor.last_name}" \
                if obj.tutor.first_name and obj.tutor.last_name \
                else obj.tutor.username
        return "Не назначен"

    tutor_col.short_description = "Репетитор"

    def student_col(self, obj):
        if obj.student:
            return f"{obj.student.first_name} {obj.student.last_name}" \
                if obj.student.first_name and obj.student.last_name \
                else obj.student.username
        return "Не назначен"

    student_col.short_description = "Ученик"

    def comment_col(self, obj):
        return obj.comment if obj.comment else "Нет комментария"
    comment_col.short_description = "Комментарий"
    comment_col.admin_order_field = 'comment'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['status'].choices = [
            ('available', 'Доступен'),
            ('pending', 'Ожидает подтверждения'),
            ('accepted', 'Принят'),
        ]
        return form

    def status_col(self, obj):
        choices = {
            'available': 'Доступен',
            'pending': 'Ожидает подтверждения',
            'accepted': 'Принят',
        }
        return choices.get(obj.status, obj.status)
    status_col.short_description = "Статус"
    status_col.admin_order_field = 'status'


__all__ = ['SlotAdmin']