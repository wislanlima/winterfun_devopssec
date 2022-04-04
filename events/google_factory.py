import datetime
import logging
import googleapiclient
from django.utils import timezone

from winterfun.calendar_connection import get_calendar_service

from winterfun.views import auth, require_auth

logger = logging.getLogger(__name__)

@require_auth
def create_cal(instance):
    print('here')
    user = instance.user.username
    print('timezone now?')
    print(timezone.get_current_timezone())
    print('##########')

    service = auth(instance)

    start_value = instance.start
    start = start_value.isoformat()
    end_value = instance.end
    end = end_value.isoformat()
    print(start_value)
    print(start)
    print('#############')
    print(type(end_value))
    print(type(end))
    print('#############')


    list = []
    attendees = instance.accounts.all()
    print(attendees)
    if attendees is not None:
        for guest in attendees:
            value = {
                'email': guest.email
            }
            list.append(value)

    # t = {"attendees": [{"email": "email@gmail.com"}, {"email": "email2@gmail.com"}]}
    # print(t)
    # print(list)
    # print(start)
    # print(end)
    # print(end.x)
    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": instance.summary,
                                               "description": instance.description,
                                               "start": {"dateTime": start, "timeZone": 'Etc/Universal'},
                                               "end": {"dateTime": end, "timeZone": 'Etc/Universal'},
                                               "attendees": list,

                                           },
                                           sendUpdates='all'
                                           ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

    print('################################')

    logger.info(f"{instance}'s Deleting events from google calendar")
    return event_result


@require_auth
def update_google_event(instance, calendar_id):
    """
    Updating the google calendar
    """

    try:
        print('here')
        user = instance.user.username
        print('timezone now?')
        print(timezone.get_current_timezone())
        print('##########')
        start_value = instance.start
        start = start_value.isoformat()
        end_value = instance.end
        end = end_value.isoformat()
        print(start_value)
        print(start)
        print('#############')
        print(type(end_value))
        print(type(end))
        print('#############')
        service = auth(instance)

        list = []
        attendees = instance.accounts.all()
        # print(attendees)
        if attendees is not None:
            for guest in attendees:
                value = {
                    'email': guest.email
                }
                list.append(value)

        start_value = instance.start
        start = start_value.isoformat()
        end_value = instance.end
        end = end_value.isoformat()

        event_result = service.events().update(
            calendarId='primary',
            eventId=calendar_id,
            body={
                "summary": 'Updated Automating calendar',
                "description": 'This is a tutorial example of automating google calendar with python, updated time.',
                "start": {"dateTime": start, "timeZone": 'Etc/Universal'},
                "end": {"dateTime": end, "timeZone": 'Etc/Universal'},
                "attendees": list,
            },
        ).execute()

        print("updated event")
        print("id: ", event_result['id'])
        print("summary: ", event_result['summary'])
        print("starts at: ", event_result['start']['dateTime'])
        print("ends at: ", event_result['end']['dateTime'])
        logger.info(f"{instance}'s a Calendar was added into you google calendar")
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

@require_auth
def update_google_event_status(instance, calendar_id, email, status):
    """
    Updating the google calendar
    """
    try:
        user = instance.user.username
        service = auth(instance)
        list_list = [{'email': email,
                      'responseStatus': status,
                      }]
        service.events().patch(
            calendarId='primary',
            eventId=calendar_id,
            body={
                "attendees": list_list,
            },
        ).execute()

    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

@require_auth
def delete_google_event(instance, calendar_id):
    # Delete the event
    user = instance.user.username
    service = auth(instance)
    try:
        service.events().delete(
            calendarId='primary',
            eventId=calendar_id,
        ).execute()
        logger.info(f"{instance}'s Deleting events from google calendar = " + calendar_id)
        return True
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")
        return False
