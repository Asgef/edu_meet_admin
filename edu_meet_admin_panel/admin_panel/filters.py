from django.contrib.admin import SimpleListFilter
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now


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
        # Текущая дата и время с учётом часового пояса
        today = now()

        if self.value() == 'Today':
            start_of_day = make_aware(
                datetime(
                    today.year, today.month, today.day,
                    0,0, 0
                )
            )
            end_of_day = make_aware(
                datetime(
                    today.year, today.month, today.day,
                    23, 59, 59
                )
            )
            return queryset.filter(date__range=(start_of_day, end_of_day))
        elif self.value() == 'Past 7 days':
            seven_days_ago = make_aware(
                datetime(
                    today.year, today.month, today.day
                ) - timedelta(days=7)
            )
            return queryset.filter(date__range=(seven_days_ago, today))
        elif self.value() == 'This month':
            start_of_month = make_aware(datetime(
                today.year, today.month, 1, 0, 0, 0
            ))
            return queryset.filter(date__range=(start_of_month, today))
        elif self.value() == 'This year':
            start_of_year = make_aware(
                datetime(
                    today.year, 1, 1, 0, 0, 0
                )
            )
            return queryset.filter(date__range=(start_of_year, today))
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
                f"{i}",
                f"Неделя {i + 1} ("
                f"{(monday + timedelta(weeks=i)).strftime('%d.%m')} - "
                f"{(monday + timedelta(weeks=i+1) - timedelta(days=1)).strftime('%d.%m')})"  # noqa
            )
            for i in range(0, 5)  # Количество недель для отображения
        ]
        return weeks

    def queryset(self, request, queryset):
        today = now()
        # Смещаем `today` к ближайшему понедельнику
        monday = today - timedelta(days=today.weekday())
        if self.value():
            try:
                week_num = int(self.value())
                start_of_week = monday + timedelta(weeks=week_num)
                end_of_week = start_of_week + timedelta(days=6, seconds=86399)
                return queryset.filter(date__range=(start_of_week, end_of_week))
            except ValueError:
                pass
        return queryset

class SpecificDateFilter(SimpleListFilter):
    title = 'Фильтр по дате'
    parameter_name = 'specific_date'

    template = 'admin/date_filter.html'

    def lookups(self, request, model_admin):
        return [
            ('', 'Все')
        ]

    def queryset(self, request, queryset):
        if self.value():
            try:
                specific_date = datetime.strptime(self.value(), '%Y-%m-%d').date()
                specific_datetime = datetime.combine(specific_date, datetime.min.time())
                specific_datetime_aware = make_aware(specific_datetime)
                return queryset.filter(date=specific_datetime_aware)
            except ValueError:
                return queryset
        return queryset


class CustomStatusFilterSlot(SimpleListFilter):
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


class CustomStatusFilterOrder(SimpleListFilter):
    title = 'Статус'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('pending', 'Ожидает подтверждения'),
            ('accepted', 'Принят'),
            ('declined', 'Отклонен'),
            ('canceled', 'Закрыт'),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

