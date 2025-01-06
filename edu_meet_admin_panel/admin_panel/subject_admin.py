from django.contrib import admin
from django import forms
from edu_meet_admin_panel.proxy_models import AcademicSubjectProxy


class SubjectChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class SubjectAdminForm(forms.ModelForm):
    class Meta:
        model = AcademicSubjectProxy
        fields = '__all__'
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'created_at': 'Дата создания',
            'updated_at': 'Последнее обновление',
        }


class AcademicSubjectAdmin(admin.ModelAdmin):
    form = SubjectAdminForm
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
