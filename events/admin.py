from django.contrib import admin

from .models import Event, CalendarEvent, EventReceiver, Relationship

# Register your models here.

admin.site.register(Event)
admin.site.register(CalendarEvent)
admin.site.register(EventReceiver)
admin.site.register(Relationship)