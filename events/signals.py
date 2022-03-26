import datetime
import logging
from django.utils import timezone

from dateutil import parser

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from events.google_factory import create_cal, update_google_event
from events.models import CalendarEvent, Event, Relationship
from winterfun.base_settings import AUTH_USER_MODEL
from winterfun.calendar_connection import get_calendar_service

logger = logging.getLogger(__name__)


# @receiver(post_save, sender=Event)
# def google_calendar_saved(sender, instance, created, **kwargs):
#     print('here, if update?')
#     if created:
#         print('does it create?')
#         logger.info(f"{instance}'s creating an event")


# @receiver(m2m_changed, sender=Event.accounts.through)
# def event_listener(sender, instance, action, **kwargs):
#     """
#     This method check and loop through all users that need to be included in the event
#
#     """
#     print('lets count action = instance')
#     print(instance)
#     print('####')
#     if action in ['post_add','post_remove','post_clear']:
#         print(timezone.now())
#         print(datetime.timedelta(seconds=5))
#         created = instance.created_at >= timezone.now() - datetime.timedelta(seconds=5)
#         if created:
#             print('Create is true')
#             """Create a google calendar"""
#             event_result = create_cal(instance)
#             """Save the google calendar id into the local database"""
#             CalendarEvent.set_google_calendar(instance, event_result['id'])
#             """set the value to true if added"""
#             instance.added_to_google_calendar = True
#             instance.save()
#             """ If the event is added we now have access to all m2m relations"""
#             Relationship.objects.set_event_relationship(instance)
#             logger.info(f"{instance}'s saving and create m2m accounts SEND into relationship table")
#
#         elif action == 'post_add':
#             print('##################AQUI atualizar o calendar')
#             """Create a google calendar"""
#
#             """Save the google calendar id into the local database"""
#             calendar_google_id = CalendarEvent.get_google_calendar(instance)
#             print(calendar_google_id)
#             update_google_event(instance, calendar_google_id)
#             #instance.save()
#             """ If the event is added we now have access to all m2m relations"""
#             Relationship.objects.set_event_relationship(instance)
#
#             logger.info(f"{instance}'s updating events and reseding emails if necessary")
#         else:
#             print(action)
#             print('here, this i snot post add')




