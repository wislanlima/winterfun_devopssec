import json
from django.core.cache import cache
from winterfun import base_settings

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
from winterfun.redis_key_schema import key_schema

SCOPES = base_settings.SCOPES
CREDENTIALS_FILE = base_settings.CREDENTIALS_FILE

TWO_DAYS = 60 * 60 * 24 * 2


def get_calendar_service(user):
    creds = None
    key_google_token = key_schema().google_token(user)
    cached_result = cache.get(key_google_token)

    if cached_result:
        result = json.loads(cached_result)
        creds = Credentials.from_authorized_user_info(result, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            cache.set(key_google_token, creds.to_json(), timeout=TWO_DAYS)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
            cache.set(key_google_token, creds.to_json(), timeout=TWO_DAYS)
        # Save the credentials for the next run


    service = build('calendar', 'v3', credentials=creds)
    return service