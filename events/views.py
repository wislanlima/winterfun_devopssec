from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
import logging
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from events.forms import EventModelForm
from events.google_factory import create_cal, update_google_event, delete_google_event, update_google_event_status
from events.models import Event, CalendarEvent, Relationship
from winterfun.views import require_auth

User = get_user_model()
logger = logging.getLogger(__name__)


class EventCreateView(LoginRequiredMixin, CreateView):
    """
    This class Create a form for the event
    It was create a form with the fields necessary for the view
    Done!
    """
    template_name = 'events/event_create.html'
    form_class = EventModelForm
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def get_success_url(self):
        """Once the event is created, it redirect to the details view"""
        return reverse("events:event-detail-view", kwargs={"id": self.object.id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        """I am adding the user that is current logger"""
        form.instance.user = self.request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super(EventCreateView, self).form_valid(form)
        """ IF the form is valid, it calls the google api for creating an event on google calendar"""
        instance = self.object
        Relationship.objects.update_event_relationship(instance)
        logger.info(f"{instance}'s saved and google calendar saved")
        return response


class EventListView(LoginRequiredMixin, ListView):
    """
    This class List all events
    Done!
    """
    model = Event
    template_name = "events/event_list.html"
    paginate_by = 4
    ordering = '-created_at'

    """apagar os dois methods de baixo, era so para enteder obj e queryset"""

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        """ print(context.keys() => dict_keys(['paginator', 'page_obj', 'is_paginated', 'object_list', 'event_list', 'view'])"""
        return context

    def get_queryset(self, *args, **kwargs):
        obj = super(EventListView, self).get_queryset(*args, **kwargs)
        # print(obj)
        return obj


class EventDetailView(LoginRequiredMixin, DetailView):
    """
    This class shows the details of the event selected
    Done!
    """
    model = Event
    template_name = "events/event_detail.html"
    slug_url_kwarg = 'id'
    slug_field = 'id'


class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):  # LoginRequiredMixin deve ser o primeiro
    """
    This class update the event details of the event selected
    it also update the google calendar event
    Return Http 404 if the user is not the owner
    Done!
    """
    model = Event
    template_name = "events/event_update.html"
    form_class = EventModelForm
    slug_url_kwarg = 'id'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs.get('id')
        context['calendar_event'] = CalendarEvent.get_google_calendar(context['object'])
        return context

    def test_func(self):
        obj = self.get_object()
        if obj.user == self.request.user:
            return True
        messages.warning(self.request, 'You need to be the owner of the event in order to update it')
        return False

    def get_success_url(self):
        # print("url")
        return reverse("events:event-detail-view", kwargs={"id": self.kwargs.get('id')})


    def form_valid(self, form):
        response = super(EventUpdateView, self).form_valid(form)
        """Update a google calendar"""
        """Save the google calendar id into the local database"""
        instance = self.object
        calendar_google_id = CalendarEvent.get_google_calendar(instance)
        if calendar_google_id:
            Relationship.objects.update_event_relationship(instance)
            update_google_event(instance, calendar_google_id)
            print('events view: calendar id existe')
        else:
            """ If the event is added we now have access to all m2m relations"""
            Relationship.objects.update_event_relationship(instance, 'send')
            print('event view: No calendar id')
        logger.info(f"{instance}'s updating events and reseding emails if necessary")
        return response

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     print("################")
    #     print("get form kwargs")
    #     kwargs.update({'id': self.kwargs.get('id')}) # self.kwargs is the kwargs passed to the view
    #     return kwargs

    # def get_object(self, *args, **kwargs):
    #     obj = super(EventUpdateView, self).get_object(*args, **kwargs)
    #     if not obj.user == self.request.user:
    #         raise Http404
    #     return obj


@require_auth
@login_required
def add_google_calendar(request):
    """
    Done
    """
    instance = None
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        try:
            instance = Event.objects.get(id=event_id)
            """event_result create a event based on the form and return the result of the api call"""
            event_result = create_cal(instance)
            """Save the google calendar id into the local database"""
            result = CalendarEvent.set_google_calendar(instance, event_result['id'])
            if result:
                """set the value to true if added"""
                instance.added_to_google_calendar = True
                instance.save()
                """ Create a relationship sent to all guests"""
                Relationship.objects.update_event_relationship(instance, 'send')
            else:
                print('IT NEEDS SOMETHING HERE FOR RE RUN IF THERE IS NO INTERNET CONNECTION WITH THE  GOOGLE API')
            logger.info(f"{instance}'s saved and google calendar saved")
        except Exception as e:
            print(str(e))
        return redirect(request.META.get("HTTP_REFERER"))
    return reverse("events:event-detail-view", kwargs={"id": instance.id})

@require_auth
@login_required
def remove_google_calendar(request):
    """
    Done
    """
    instance = None
    if request.method == "POST":
        event_id = request.POST.get("event_id")
        try:
            instance = Event.objects.get(id=event_id)
            calendar_google_id = CalendarEvent.get_google_calendar(instance)
            """Remove From my Google account"""
            result = delete_google_event(instance, calendar_google_id)
            if result:
                """If the id is tru, remove from my local database"""
                CalendarEvent.delete_google_calendar(instance)
                """update my events that I can recreate a new request"""
                instance.added_to_google_calendar = False
                instance.save()
            else:
                print('IT NEEDS SOMETHING HERE FOR RE RUN IF THERE IS NO INTERNET CONNECTION WITH THE  GOOGLE API')
            messages.success(request, 'You have removed this event from your google calendar')
            logger.info(f"{instance}'s The google calendar was removed?")
        except Exception as e:
            print(str(e))
        return redirect(request.META.get("HTTP_REFERER"))
    return reverse("events:event-detail-view", kwargs={"id": instance.id})


@login_required
def update_guest_status(request):
    """
    List of request send to my_profile where the status is send(Here the user can decide to accept is or reject
    key: winterfun:user:username
    Done
    """
    instance = None
    if request.method == "POST":
        event_pkid = request.POST.get("event_pkid")
        user_pkid = request.POST.get("user_pkid")
        status = request.POST.get("status_id")
        try:
            query_set = Relationship.objects.update_object_status(event_pkid, user_pkid, status)
            email = request.user.email
            event = Event.objects.get(pkid=event_pkid)
            calendar_google_id = CalendarEvent.get_google_calendar(event_pkid)
            if calendar_google_id:
                update_google_event_status(event, calendar_google_id, email, status)
        except Exception as e:
            print(str(e))
            print("nao functionou")
        return redirect(request.META.get("HTTP_REFERER"))
    return reverse("events:event-detail-view", kwargs={"id": instance.id})


class EventDeleteView(LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView):
    """
    This class delete the event and remove the calendar from the owner

    Return Http 404 if the user is not the owner

    Done!
    """
    model = Event
    success_message = " Deleted successfully"
    slug_url_kwarg = 'id'
    slug_field = 'id'
    success_url = reverse_lazy('events:event-list')

    # def get_object(self, *args, **kwargs):
    #     obj = super(EventDeleteView, self).get_object(*args, **kwargs)
    #     if not obj.user == self.request.user:
    #         raise Http404
    #     return obj

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        messages.success(self.request, self.success_message % instance.__dict__)
        try:
            calendar_google_id = CalendarEvent.get_google_calendar(instance)
            # print(calendar_google_id)
            delete_google_event(instance, calendar_google_id)
        except Exception as e:
            print('Google Calendar doesnt exist')
        return super(EventDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        obj = self.get_object()
        if obj.user == self.request.user:
            return True
        messages.warning(self.request, 'You need to be the author of the event in order to delete it')
        return False


#
# def create_event(request):
#     if request.method == 'POST':
#         form = EventModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('events:event-list')
#     else:
#         form = EventModelForm()
#     return render(request, 'events/home.html', {'form': form})


def my_events(request):
    """
    This function display the events details of the user.

    Done!
    """
    context = {}
    user = request.user
    events = Event.get_my_events(user)
    context['events'] = events

    return render(request, "events/my_events.html", context)


def guests(users):
    return redirect("profiles:my-profile")
