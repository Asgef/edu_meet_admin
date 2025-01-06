from django.contrib import admin
from edu_meet_admin_panel.admin_panel import (
    SlotAdmin, OrderAdmin, UserAdmin, AcademicSubjectAdmin
)
from edu_meet_admin_panel.proxy_models import (
    OrderProxy, UserProxy, SlotProxy, AcademicSubjectProxy
)


# Словарь: модель -> класс админки
CUSTOM_ADMINS = {
    'OrderProxy': OrderAdmin,
    'UserProxy': UserAdmin,
    'SlotProxy': SlotAdmin,
    'AcademicSubjectProxy': AcademicSubjectAdmin
}


# Регистрация прокси-моделей
for model in [OrderProxy, UserProxy, SlotProxy, AcademicSubjectProxy]:
    if not admin.site.is_registered(model):
        admin.site.register(model, CUSTOM_ADMINS[model.__name__])
