from django.contrib import admin
from django.apps import apps

# Настройка отображения полей в админке
class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_available', 'date', 'time_start', 'time_end', 'tutor', 'student', 'comment')
    search_fields = ('tutor__username', 'student__username', 'comment')
    list_filter = ('is_available', 'date')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'tutor', 'slot', 'subject', 'status', 'date', 'comment')
    search_fields = ('student__username', 'tutor__username', 'comment')
    list_filter = ('status',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'tg_id', 'username', 'is_admin', 'timezone', 'first_name', 'last_name', 'created_at')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_admin',)

# Словарь: модель -> класс админки
CUSTOM_ADMINS = {
    'Slot': SlotAdmin,
    'Order': OrderAdmin,
    'User': UserAdmin,
}

# Динамическая регистрация моделей
MODELS_TO_INCLUDE = ['Slot', 'Order', 'User']
app_models = apps.get_app_config('edu_meet_admin_panel').get_models()

for model in app_models:
    if model.__name__ in MODELS_TO_INCLUDE:
        if not admin.site.is_registered(model):
            admin_class = CUSTOM_ADMINS.get(model.__name__, admin.ModelAdmin)
            admin.site.register(model, admin_class)
