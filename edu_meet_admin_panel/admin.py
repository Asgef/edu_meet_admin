from django.contrib import admin
from schedule.models import Calendar, Event, Occurrence
from edu_meet_admin_panel.models import Slot, Order, User

admin.site.register(Calendar)
admin.site.register(Event)
admin.site.register(Occurrence)
admin.site.register(Slot)
admin.site.register(Order)
admin.site.register(User)
