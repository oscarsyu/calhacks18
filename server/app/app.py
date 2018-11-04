from logging.config import dictConfig

from flask import Blueprint, json, Response, redirect, request

from app import spotify

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

bp = Blueprint('app', __name__)


@bp.route('/')
def index():
    return 'Hey this is working!'


@bp.route('/spotify/auth')
def spotify_auth():
    return redirect(spotify.auth_url())


@bp.route('/spotify/logout')
def spotify_logout():
    return redirect(spotify.logout_url())


@bp.route('/spotify/callback')
def spotify_callback():
    access_token = spotify.authorize(request.args.get('code')) or ''

    if access_token:
        # hash = hashlib.sha1()
        # hash.update(str(time.time()).encode('utf-8'))
        # hash.hexdigest()
        # user_id = hash.hexdigest()
        user_id = access_token
    else:
        user_id = ''

    return Response(
        '''<script type="text/javascript">
// Thanks to: https://www.phodal.com/blog/react-native-onmessage-couldnt-read-postmessage-issue/

function awaitPostMessage() {
  var isReactNativePostMessageReady = !!window.originalPostMessage;
  var queue = [];
  var currentPostMessageFn = function store(message) {
    if (queue.length > 100) queue.shift();
    queue.push(message);
  };
  if (!isReactNativePostMessageReady) {
    var originalPostMessage = window.postMessage;
    Object.defineProperty(window, 'postMessage', {
      configurable: true,
      enumerable: true,
      get: function () {
        return currentPostMessageFn;
      },
      set: function (fn) {
        currentPostMessageFn = fn;
        isReactNativePostMessageReady = true;
        setTimeout(sendQueue, 0);
      }
    });
    window.postMessage.toString = function () {
      return String(originalPostMessage);
    };
  }

  function sendQueue() {
    while (queue.length > 0) window.postMessage(queue.shift());
  }
}

window.onload = function () {
    awaitPostMessage();
    
    const USER_ID = '%s';
    document.write('Here is your user id: ' + USER_ID + '<br>');
    window.postMessage(USER_ID);
    document.write('The page should disappear soon :o');
};
</script>''' % user_id,
        'text/html'
    )


@bp.route('/mock/playlists/<string:mood>')
def mock_playlist(mood):
    """
    Some mock data available at
        /mock/playlists/happy
        /mock/playlists/sad
    """

    mock_playlists = {
        'happy': [
            'Happy song 1',
            'Happy song 2',
        ],
        'sad': [
            'Sad song 1',
            'Sad song 2',
        ],
    }

    return Response(json.dumps(mock_playlists[mood] if mood in mock_playlists else []), 'application/json')


@bp.route('/mock/auth/echo-authorization')
def mock_auth_echo_authorization():
    return request.headers.get('Authorization', '')
