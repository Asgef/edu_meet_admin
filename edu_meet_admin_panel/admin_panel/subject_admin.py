from django.contrib import admin
from django.apps import apps


class AcademicSubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name_col', 'description_col', 'created_at', 'updated_at'
    )
    search_fields = ('name', 'description')


    def name_col(self, obj):
        return obj.name if obj.name else "Не указан"
    name_col.short_description = "Наименование"
    name_col.admin_order_field = 'name'

    def description_col(self, obj):
        return obj.description if obj.description else "Не указан"
    description_col.short_description = "Описание"
    description_col.admin_order_field = 'description'

__all__ = ['AcademicSubjectAdmin']