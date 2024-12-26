from django.contrib import admin
from edu_meet_admin_panel.admin_panel.slot_admin import SlotChoiceField
from edu_meet_admin_panel.admin_panel.user_admin import UserChoiceField
from edu_meet_admin_panel.models import User, Order, AcademicSubject, Slot
from edu_meet_admin_panel.proxy_models import SlotProxy
from django import forms
from edu_meet_admin_panel.admin_panel.subject_admin import SubjectChoiceField

class OrderAdminForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('accepted', 'Принят'),
        ('declined', 'Отклонен'),
        ('canceled', 'Закрыт'),
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Статус")

    tutor = UserChoiceField(
        queryset=User.objects.all(),
        label="Репетитор"
    )
    student = UserChoiceField(
        queryset=User.objects.all(),
        label="Ученик",
        required=False
    )
    subject = SubjectChoiceField(
        queryset= AcademicSubject.objects.all(),
        label="Предмет"
    )
    slot = SlotChoiceField(
        queryset=SlotProxy.objects.all(),
        label="Слот"
    )
    comment = forms.CharField(
        widget=forms.Textarea,
        label="Комментарий",
        required=False
    )

    class Meta:
        model = Order
        fields = '__all__'
        labels = {
            'date': 'Дата',
            'created_at': 'Дата создания',
            'updated_at': 'Последнее обновление',
            'slot': 'Слот',
            'comment': 'Комментарий',
            'status': 'Статус',
            'subject': 'Предмет',
            'tutor': 'Репетитор',
            'student': 'Ученик',
        }

class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
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
        return (
            f"{obj.slot.id} {obj.slot.date} "
            f"{obj.slot.time_start.strftime('%H:%M')}"
        ) if obj.slot else "Нет слота"
    slot_col.short_description = "Слот"
    slot_col.admin_order_field = 'slot__id'

    def subject_col(self, obj):
        return obj.subject.name if obj.subject else "Без предмета"
    subject_col.short_description = "Предмет"
    subject_col.admin_order_field = 'subject__name'

    def status_col(self, obj):
        choices = {
            'pending': 'Ожидает подтверждения',
            'accepted': 'Принят',
            'declined': 'Отклонен',
            'canceled': 'Закрыт',
        }
        return choices.get(obj.status, obj.status)
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