from django.urls import path

from django.conf.urls import url
from events import views
from events.views import update_guest_status, add_google_calendar, remove_google_calendar, my_events, EventListView, EventDetailView, EventUpdateView, \
    EventCreateView, EventDeleteView

app_name = "events"

urlpatterns = [
    path('my_events/', my_events, name='my-events'),
    path("list/", EventListView.as_view(), name="event-list"),
    path("create/", EventCreateView.as_view(), name="event-create-view"),
    path("detail/<id>/", EventDetailView.as_view(), name="event-detail-view"),
    path("update/<id>/", EventUpdateView.as_view(), name="event-update-view"),
    path("delete/<id>/", EventDeleteView.as_view(), name="event-delete-view"),
    path("add_calendar/", add_google_calendar, name="add-google-calendar"),
    path("remove_calendar/", remove_google_calendar, name="remove-google-calendar"),
    path("update_status/", update_guest_status, name="update-guest-status"),
]
