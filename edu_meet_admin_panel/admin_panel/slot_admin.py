from django.contrib import admin
from edu_meet_admin_panel.models import Slot
from django import forms


class SlotAdminForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('pending', 'Ожидает подтверждения'),
        ('accepted', 'Принят'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")

    class Meta:
        model = Slot
        fields = '__all__'

class SlotAdmin(admin.ModelAdmin):
    form = SlotAdminForm
    list_display = (
        'id', 'status_col', 'date_col', 'time_start_col',
        'time_end_col', 'tutor_col', 'student_col', 'comment_col'
    )
    search_fields = ('tutor__username', 'student__username', 'comment')
    list_filter = ('status', 'date')

    def status_col(self, obj):
        return obj.status
    status_col.short_description = "Статус"
    status_col.admin_order_field = 'status'

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
        return obj.tutor.username if obj.tutor else "Не назначен"
    tutor_col.short_description = "Репетитор"
    tutor_col.admin_order_field = 'tutor__username'

    def student_col(self, obj):
        return obj.student.username if obj.student else "Не назначен"
    student_col.short_description = "Ученик"
    student_col.admin_order_field = 'student__username'

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