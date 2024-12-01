from django.contrib import admin
from django.apps import apps

# Настройка отображения полей в админке
class SlotAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_col', 'date_col', 'time_start_col', 'time_end_col', 'tutor_col', 'student_col', 'comment_col')
    search_fields = ('tutor__username', 'student__username', 'comment')
    list_filter = ('status', 'date')

    def status_col(self, obj):
        return obj.status
    status_col.short_description = "Статус"
    status_col.admin_order_field = 'status'

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
        return obj.tutor.username if obj.tutor else "Не назначен"
    tutor_col.short_description = "Репетитор"
    tutor_col.admin_order_field = 'tutor__username'

    def student_col(self, obj):
        return obj.student.username if obj.student else "Не назначен"
    student_col.short_description = "Ученик"
    student_col.admin_order_field = 'student__username'

    def comment_col(self, obj):
        return obj.comment if obj.comment else "Нет комментария"
    comment_col.short_description = "Комментарий"
    comment_col.admin_order_field = 'comment'



class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_col', 'tutor_col', 'slot_col', 'subject_col', 'status_col', 'date_col', 'comment_col')
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



class UserAdmin(admin.ModelAdmin):
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
