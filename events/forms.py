from django import forms
from django.contrib.admin import widgets

from .models import Event, CalendarEvent, EventReceiver



from .widgets import XDSoftDateTimePickerInput



class EventModelForm(forms.ModelForm):
    start = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput()
    )
    end = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=XDSoftDateTimePickerInput()
    )

    class Meta:
        model = Event
        fields = ['summary', 'description', 'start', 'end', 'accounts']



class CalendarEventModelForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['calendar_event_id', 'event']


class EventReceiverModelForm(forms.ModelForm):
    class Meta:
        model = EventReceiver
        fields = ['event', 'account', 'opened', 'clicked']


