import datetime
import logging
import googleapiclient
from django.utils import timezone

from winterfun.calendar_connection import oauth2callback, require_auth

logger = logging.getLogger(__name__)

@require_auth
def create_cal(instance):
    """
    This method check the wrap function if the user has a valid token from redis
     if it doesnt, it creates a link for authentication with google
     once the user has given permision to access the calendar, we have a valid token and we can call the command using the method build
     We use an instance of the event that hold the same fields that we can use to update the event on google calendar.
    Done!
    """
    # Get the authentication from the calendar_connection.py
    service = oauth2callback(instance)

    # get the values from the current object
    start_value = instance.start
    start = start_value.isoformat()
    end_value = instance.end
    end = end_value.isoformat()

    list = []
    attendees = instance.accounts.all()
    if attendees is not None:
        for guest in attendees:
            value = {
                'email': guest.email
            }
            list.append(value)

    # Send the command to save the event on google
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

    # print("created event")
    # print("id: ", event_result['id'])
    # print("summary: ", event_result['summary'])
    # print("starts at: ", event_result['start']['dateTime'])
    # print("ends at: ", event_result['end']['dateTime'])

    logger.info(f"{instance}'s Deleting events from google calendar")
    return event_result


@require_auth
def update_google_event(instance, calendar_id):
    """
    This method uses the wrap function if the user has a valid token from redis
     if it doesnt, it creates a link for authentication with google
     once the user has given permision to access the calendar, we have a valid token and we can call the command using the method build
     We use an instance of the event that to update the same fields that we can use to update the event on google calendar.
    Done!
    """

    try:
        service = oauth2callback(instance)

        start_value = instance.start
        start = start_value.isoformat()
        end_value = instance.end
        end = end_value.isoformat()


        list = []
        attendees = instance.accounts.all()
        # print(attendees)
        if attendees is not None:
            for guest in attendees:
                value = {
                    'email': guest.email
                }
                list.append(value)

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

        # print("updated event")
        # print("id: ", event_result['id'])
        # print("summary: ", event_result['summary'])
        # print("starts at: ", event_result['start']['dateTime'])
        # print("ends at: ", event_result['end']['dateTime'])
        logger.info(f"{instance}'s a Calendar was added into you google calendar")
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

@require_auth
def update_google_event_status(instance, calendar_id, email, status):
    """
    This method uses the wrap function if the user has a valid token from redis
     if it doesnt, it creates a link for authentication with google
     once the user has given permision to access the calendar, we have a valid token and we can call the command using the method build

     We update the reply from the user with the status of refusing or accepting the meeting
    Done!
    """
    try:

        service = oauth2callback(instance)
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
    """
    This method uses the wrap function if the user has a valid token from redis
     if it doesnt, it creates a link for authentication with google
     once the user has given permision to access the calendar, we have a valid token and we can call the command using the method build

    The owner of the meeting can delete from google calendar
    Done!
    """

    service = oauth2callback(instance)
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
