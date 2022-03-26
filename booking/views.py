from __future__ import print_function
from django.shortcuts import render


import datetime
import os.path
import json
from django.core.cache import cache
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
from winterfun.calendar_connection import get_calendar_service
from winterfun.redis_key_schema import key_schema

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

ONE_HOUR = 60 * 60


# Create your views here.
def index(request):
    user = request.user

    try:
        service = get_calendar_service(user)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except Exception as e:
        print('An error occurred: %s' + str(e))
    return render(request, "booking/index.html", {})
