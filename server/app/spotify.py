import base64
import logging
import os
import urllib.parse
import requests

from flask import current_app, json

from app.base import BASE_URL

SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL + '/authorize'
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL + '/api/token'

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

CLIENT_BEARER = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode()).decode()

SCOPE = [
    'playlist-modify-public'
]

CALLBACK_URL = BASE_URL + '/spotify/callback'
AUTH_URL = BASE_URL + '/spotify/auth'

logger = logging.getLogger(__name__)


def build_query_params(d):
    return '&'.join('{}={}'.format(k, urllib.parse.quote(v)) for k, v in d.items())


def auth_url():
    return '{}?{}'.format(SPOTIFY_AUTH_URL, build_query_params({
        'response_type': 'code',
        'redirect_uri': CALLBACK_URL,
        'scope': ' '.join(SCOPE),
        'client_id': CLIENT_ID
    }))


def logout_url():
    return 'https://spotify.com/logout'


def authorize(auth_token):
    headers = {
        'Authorization': 'Basic {}'.format(CLIENT_BEARER)
    }
    payload = {
        'grant_type': 'authorization_code',
        'code': auth_token,
        'redirect_uri': CALLBACK_URL
    }

    request = requests.post(SPOTIFY_TOKEN_URL, data=payload, headers=headers)

    response_data = json.loads(request.text)
    current_app.logger.info('response_data=' + str(response_data))
    if 'error' in response_data:
        return None
    return response_data['access_token']
