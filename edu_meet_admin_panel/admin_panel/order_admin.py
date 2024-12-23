from django.contrib import admin
from django.apps import apps


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'student_col', 'tutor_col', 'slot_col', 'subject_col',
        'status_col', 'date_col', 'comment_col'
    )
    search_fields = ('student__username', 'tutor__username', 'comment')
    list_filter = ('status',)

    def student_col(self, obj):
        return obj.student.username if obj.student else "Не назначен"
    student_col.short_description = "Ученик"
    student_col.admin_order_field = 'student__username'

    def tutor_col(self, obj):
        return obj.tutor.username if obj.tutor else "Не назначен"
    tutor_col.short_description = "Репетитор"
    tutor_col.admin_order_field = 'tutor__username'

    def slot_col(self, obj):
        return f"Слот {obj.slot.id}" if obj.slot else "Нет слота"
    slot_col.short_description = "Слот"
    slot_col.admin_order_field = 'slot__id'

    def subject_col(self, obj):
        return obj.subject.name if obj.subject else "Без предмета"
    subject_col.short_description = "Предмет"
    subject_col.admin_order_field = 'subject__name'

    def status_col(self, obj):
        return obj.status
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

__all__ = ['OrderAdmin']