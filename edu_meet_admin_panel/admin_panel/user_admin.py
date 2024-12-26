from django.contrib import admin
from django import forms
from edu_meet_admin_panel.models import User
from django.apps import apps


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        username = obj.username
        first_name = obj.first_name
        last_name = obj.last_name

        if first_name and last_name:
            return f"{first_name} {last_name}"
        return username


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        labels = {
            'username': 'Никнейм',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'is_admin': 'Администратор',
            'timezone': 'Часовой пояс',
            'last_activity': 'Последняя активность',
            'created_at': 'Дата регистрации',
            'updated_at': 'Последнее обновление',
        }



class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = (
        'id', 'tg_id', 'username_col', 'is_admin_col', 'timezone',
        'first_name_col', 'last_name_col', 'created_at_col'
    )
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_admin',)

    def username_col(self, obj):
        return obj.username if obj.username else "Не указан"
    username_col.short_description = "Логин"
    username_col.admin_order_field = 'username'

    def first_name_col(self, obj):
        return obj.first_name if obj.first_name else "Не указан"
    first_name_col.short_description = "Имя"
    first_name_col.admin_order_field = 'first_name'

    def last_name_col(self, obj):
        return obj.last_name if obj.last_name else "Не указан"
    last_name_col.short_description = "Фамилия"
    last_name_col.admin_order_field = 'last_name'

    def is_admin_col(self, obj):
        return "Администратор" if obj.is_admin else "Пользователь"
    is_admin_col.short_description = "Роль"
    is_admin_col.admin_order_field = 'is_admin'

    def created_at_col(self, obj):
        return obj.created_at.strftime("%d.%m.%Y %H:%M")
    created_at_col.short_description = "Дата создания"
    created_at_col.admin_order_field = 'created_at'


__all__ = ['UserAdmin']
