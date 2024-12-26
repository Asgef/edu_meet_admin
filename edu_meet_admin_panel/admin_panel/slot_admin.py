from django.contrib import admin
from edu_meet_admin_panel.admin_panel.user_admin import UserChoiceField
from edu_meet_admin_panel.models import Slot
from edu_meet_admin_panel.proxy_models import UserProxy
from django import forms
from django.contrib.admin import SimpleListFilter
from django.utils.timezone import now
from datetime import datetime, timedelta


# Кастомный фильтр по дате
class CustomDateFilter(SimpleListFilter):
    title = 'Дата'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return [
            ('Any', 'Любая'),
            ('Today', 'Сегодня'),
            ('Past 7 days', 'За последние 7 дней'),
            ('This month', 'Этот месяц'),
            ('This year', 'Этот год'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'Today':
            today = now().date()
            return queryset.filter(date=today)
        elif self.value() == 'Past 7 days':
            today = now().date()
            seven_days_ago = today - timedelta(days=7)
            return queryset.filter(date__range=(seven_days_ago, today))
        elif self.value() == 'This month':
            today = now()
            start_of_month = today.replace(day=1).date()
            return queryset.filter(date__range=(start_of_month, today.date()))
        elif self.value() == 'This year':
            today = now()
            start_of_year = today.replace(month=1, day=1).date()
            return queryset.filter(date__range=(start_of_year, today.date()))
        elif self.value() == 'Any':
            return queryset
        return queryset


class FutureWeeksFilter(SimpleListFilter):
    title = 'Будущие недели'
    parameter_name = 'future_week'

    def lookups(self, request, model_admin):
        today = now().date()
        # Смещаем `today` к ближайшему понедельнику
        monday = today - timedelta(days=today.weekday())
        weeks = [
            (
                f"week_{i}",
                f"Неделя {i + 1} ({(monday + timedelta(weeks=i)).strftime('%d.%m')} - "
                f"{(monday + timedelta(weeks=i+1) - timedelta(days=1)).strftime('%d.%m')})"
            )
            for i in range(0, 5)  # Количество недель для отображения
        ]
        return weeks

    def queryset(self, request, queryset):
        today = now().date()
        # Смещаем `today` к ближайшему понедельнику
        monday = today - timedelta(days=today.weekday())
        if self.value():
            try:
                week_num = int(self.value().split('_')[1])
                start_of_week = monday + timedelta(weeks=week_num)
                end_of_week = start_of_week + timedelta(days=6)
                return queryset.filter(date__range=(start_of_week, end_of_week))
            except (ValueError, IndexError):
                pass
        return queryset


class SpecificDateFilter(SimpleListFilter):
    title = 'Фильтр по дате'  # Заголовок фильтра
    parameter_name = 'specific_date'

    template = 'admin/date_filter.html'  # Свой шаблон для фильтра

    def lookups(self, request, model_admin):
        return [
            ('', 'Все')
        ]

    def queryset(self, request, queryset):
        if self.value():
            try:
                specific_date = datetime.strptime(self.value(), '%Y-%m-%d').date()
                return queryset.filter(date=specific_date)
            except ValueError:
                return queryset
        return queryset


class CustomStatusFilter(SimpleListFilter):
    title = 'Статус'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('available', 'Доступен'),
            ('pending', 'Ожидает подтверждения'),
            ('accepted', 'Принят'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

# Пользовательский фильтр по часу начала
class HourStartFilter(SimpleListFilter):
    title = 'Час начала'
    parameter_name = 'hour_start'

    def lookups(self, request, model_admin):
        return [
            (str(i), f"{i}:00") for i in range(0, 24)
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(time_start__hour=int(self.value()))
        return queryset


class SlotChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return (f"{obj.date} {obj.time_start.strftime('%H:%M')} - "
                f"{obj.time_end.strftime('%H:%M')}")


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
        'id', 'status_col', 'date_col', 'time_start_col',
        'time_end_col', 'tutor_col', 'student_col', 'comment_col'
    )
    search_fields = ('tutor__username', 'student__username', 'comment')
    list_filter = (
        CustomStatusFilter, CustomDateFilter, HourStartFilter,
        FutureWeeksFilter, SpecificDateFilter
    )

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