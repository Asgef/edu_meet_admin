from django.contrib.admin import SimpleListFilter
from django.utils.timezone import now
from datetime import datetime, timedelta
from django import forms


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