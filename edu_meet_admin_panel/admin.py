from django.contrib import admin
from django.apps import apps
from edu_meet_admin_panel.admin_panel import (
    SlotAdmin, OrderAdmin, UserAdmin, AcademicSubjectAdmin
)


# Словарь: модель -> класс админки
CUSTOM_ADMINS = {
    'Slot': SlotAdmin,
    'Order': OrderAdmin,
    'User': UserAdmin,
    'AcademicSubject': AcademicSubjectAdmin
}

# Динамическая регистрация моделей
MODELS_TO_INCLUDE = ['Slot', 'Order', 'User', 'AcademicSubject']
app_models = apps.get_app_config('edu_meet_admin_panel').get_models()

for model in app_models:
    if model.__name__ in MODELS_TO_INCLUDE:
        if not admin.site.is_registered(model):
            admin_class = CUSTOM_ADMINS.get(model.__name__, admin.ModelAdmin)
            admin.site.register(model, admin_class)
