from rest_framework import serializers
from .models import Event, CalendarEvent
from users.serializers import UserSerializer


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = (
            'calendar_event_id',
            'event',
        )

class EventSerializer(serializers.ModelSerializer):
    accounts = UserSerializer(many=True, required=False)
    calendar_event_events = CalendarEventSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = (
            'user',
            'summary',
            'description',
            'start',
            'end',
            'accounts',
            'calendar_event_events'
        )
