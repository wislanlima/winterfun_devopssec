import json
from django.core.cache import cache
from django.shortcuts import render, redirect
from winterfun import base_settings
from winterfun.redis_key_schema import key_schema
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build



SCOPES = base_settings.SCOPES
CREDENTIALS_FILE = base_settings.CREDENTIALS_FILE
REDIRECT_URI = 'http://127.0.0.1:8000/oauth2callback/'
flow = Flow.from_client_secrets_file(
    CREDENTIALS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI)

TWO_DAYS = 60 * 60 * 24 * 2

def require_auth(function):
    """
    This function is used to check the google credentials, it checks the credential on redis if doesn't exist,
    create a new url for login into google api
    Done!
    """
    def wrapper(request, *args, **kwargs):
        creds = None
        user = request.user
        key_google_token = key_schema().google_token(user)
        cached_result = cache.get(key_google_token)
        # If there is an active user on cache (i.e. a user is logged in)
        if cached_result:
            ## 1. Using Google API Client library ##
            result = json.loads(cached_result)
            creds = Credentials.from_authorized_user_info(result, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                cache.set(key_google_token, creds.to_json(), timeout=TWO_DAYS)
                # print('count the number of times this function was called')
                return function(request, *args, **kwargs)
            else:
                # Create a personalized url for authentication
                auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
                print(auth_url)
                return redirect(auth_url)
        else:
            return function(request, *args, **kwargs)
    return wrapper

def oauth2callback(request):
    """
    This function is the call back function. There is a url(it was configured on the Calendar API) that is redirect from google back to the aplication with the user's token
    Use caches to check if the user has a valid token
    Done!
    """
    user = request.user
    key_google_token = key_schema().google_token(user)
    cached_result = cache.get(key_google_token)
    if cached_result:
        # print('the user is on cache')
        result = json.loads(cached_result)
        creds = Credentials.from_authorized_user_info(result, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        # Construct a Resource to interact with the Drive API using the values from cache
        return service
    try:
        # If the user is logging for the first time
        # Get the authorization code, that is provided as a
        # GET parameter passed to the redirect URI,
        # after consent is granted by the user.
        code = request.GET.get('code','')
        flow.fetch_token(code=code)
        json_creds = flow.credentials.to_json()
        cache.set(key_google_token, json_creds, timeout=TWO_DAYS)
        service = build('calendar', 'v3', credentials=json_creds)
        return service
    # If the '/auth' URL is not requested (with valid parameters)
    # in a OAuth2 authentication flow, redirect to home page
    except Exception as e:
        return redirect('/')
    return redirect('/')