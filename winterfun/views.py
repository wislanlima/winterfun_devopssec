import json
from django.core.cache import cache
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import render, redirect
from winterfun import base_settings
from winterfun.redis_key_schema import key_schema
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = base_settings.SCOPES
CREDENTIALS_FILE = base_settings.CREDENTIALS_FILE
REDIRECT_URI = 'http://127.0.0.1:8000/auth/'
flow = Flow.from_client_secrets_file(
    CREDENTIALS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI)

TWO_DAYS = 60 * 60 * 24 * 2

def require_auth(function):
    def wrapper(request, *args, **kwargs):
        creds = None
        user = request.user
        key_google_token = key_schema().google_token(user)
        cached_result = cache.get(key_google_token)
        if cached_result:
            result = json.loads(cached_result)
            creds = Credentials.from_authorized_user_info(result, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                cache.set(key_google_token, creds.to_json(), timeout=TWO_DAYS)
                print('here?')
                return function(request, *args, **kwargs)
            else:
                # If in doubt, just logout to clear session and cookies.
                print('HERE logout(request)')
                auth_url, _ = flow.authorization_url(prompt='consent')
                return redirect(auth_url)
        else:
            return function(request, *args, **kwargs)
    return wrapper

@require_auth
def wislan(request):
    service = auth(request)

    print('viw from settings wislan')
    return render(request, "frontend/index.html", {})

# def google_login(request):
#     user = request.user
#     key_google_token = key_schema().google_token(user)
#     cached_result = cache.get(key_google_token)
#     if cached_result:
#         print('js existe valor no cache')
#         result = json.loads(cached_result)
#         creds = Credentials.from_authorized_user_info(result, SCOPES)
#         return redirect('/')
#     else:
#         # Get the authorization URL and redirect to it.
#         auth_url, _ = flow.authorization_url(prompt='consent')
#         return redirect(auth_url)
#TODO AQUI ONDE EU PARO O CTRZ



def auth(request):

    user = request.user
    key_google_token = key_schema().google_token(user)
    cached_result = cache.get(key_google_token)
    if cached_result:
        print('js existe valor no cache')
        result = json.loads(cached_result)
        creds = Credentials.from_authorized_user_info(result, SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        return service

    try:
        # Get the authorization code, that is provided as a
        # GET parameter passed to the redirect URI,
        # after consent is granted by the user.
        code = request.GET.get('code','')

        # Use the authorization code to get (fetch) the access token.
        flow.fetch_token(code=code)

        # Create a JSON string representation of the Credentials
        # object containing (among other items) the access token
        # that has just been fetched.
        json_creds = flow.credentials.to_json()
        cache.set(key_google_token, json_creds, timeout=TWO_DAYS)
        # Convert the JSON representation of the Credentials object
        # to a Python dictionary, in order to store it as a session key.
        dict_creds = json.loads(json_creds)
        service = build('calendar', 'v3', credentials=json_creds)
        return service
    # If the '/auth' URL is not requested (with valid parameters)
    # in a OAuth2 authentication flow, redirect to home page
    except Exception as e:
        return redirect('/')
    return redirect('/')





