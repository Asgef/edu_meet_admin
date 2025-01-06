try:
    from edu_meet_admin_panel.admin_panel.slot_admin import SlotAdmin
    from edu_meet_admin_panel.admin_panel.order_admin import OrderAdmin
    from edu_meet_admin_panel.admin_panel.user_admin import UserAdmin
    from edu_meet_admin_panel.admin_panel.subject_admin import AcademicSubjectAdmin # noqa E501
except ImportError:
    SlotAdmin = None
    OrderAdmin = None
    UserAdmin = None
    AcademicSubjectAdmin = None

__all__ = [
    "SlotAdmin",
    "OrderAdmin",
    "UserAdmin",
    "AcademicSubjectAdmin",
]

# Обход проблем с импортами при генерации models.py
