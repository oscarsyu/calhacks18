import pickle
from logging.config import dictConfig
import pandas as pd
import numpy as np
from flask import Blueprint, json, Response, redirect, request, current_app

from app import spotify
from app.base import RELEASE_CHANNEL

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
        'level': 'DEBUG' if RELEASE_CHANNEL == 'dev' else 'INFO',
        'handlers': ['wsgi']
    }
})

bp = Blueprint('app', __name__)


def get_access_token():
    return request.headers.get('Authorization', '')


@bp.route('/')
def index():
    return 'Hey this is working!'


with open('app/lm.pickle', 'rb') as fi:
    lm = pickle.load(fi)


@bp.route('/playlist/create')
def playlist_create():
    access_token = get_access_token()
    mood = float(request.args.get('mood'))

    if not access_token:
        return '{"error":"Not authorized"}', 403

    # Getting all tracks

    current_app.logger.info('Getting all tracks')

    all_tracks = spotify.get_all_tracks(access_token, 100)

    current_app.logger.info('Getting features')

    all_tracks_features = spotify.get_audio_features(access_token, all_tracks)
    [track.update(features) for track, features in zip(all_tracks, all_tracks_features)]

    # Classifying things

    current_app.logger.info('Classifying things')

    data = pd.DataFrame.from_dict(all_tracks)
    new_labels = {'tempo': 'bpm', 'danceability': 'dnce', 'energy': 'nrgy', 'loudness': 'dB', 'liveliness': 'live',
                  'valence': 'val', 'duration_ms': 'dur', 'acousticness': 'acous'}
    data = data.rename(columns=new_labels)

    def prep_data(frame):
        frame_data = frame
        # zero_bpm = frame_data[frame_data['bpm'] == 0].index[0]
        # frame_data = frame_data.drop([zero_bpm])
        frame_data['dur'] = frame_data['dur'].astype('float')
        return frame_data

    def normalize(col):
        col_range = max(col) - min(col)
        avg = np.mean(col)
        return (col - avg) / col_range

    def prep_features(tbl):
        tbl_norm = tbl
        tbl_norm['bpm'] = normalize(tbl_norm['bpm'])
        tbl_norm['nrgy'] = normalize(tbl_norm['nrgy'] * 100)
        tbl_norm['dnce'] = normalize(tbl_norm['dnce'] * 100)
        tbl_norm['val'] = normalize(tbl_norm['val'] * 100)
        tbl_norm['acous'] = normalize(tbl_norm['acous'] * 100)
        tbl_norm['dur'] = tbl_norm['dur'] / 100000
        return tbl_norm

    data = prep_data(data)
    data = prep_features(data)

    def predict_songs(tbl):
        tbl_predicted = tbl
        predicted = lm.predict(tbl.loc[:, ['bpm', 'nrgy', 'dnce', 'dB', 'val', 'dur', 'acous']])
        tbl_predicted['mood_predicted'] = predicted
        return tbl_predicted

    predicted = predict_songs(data)

    def find_predicted_songs(tbl, score, num_songs):
        songs = num_songs
        if songs > 25:
            songs = 25
        in_range = tbl

        in_range['dists'] = abs(in_range['mood_predicted'] - score)
        sort_by_dist = in_range.sort_values('dists')

        return sort_by_dist[:num_songs]

    playlist = find_predicted_songs(predicted, mood, 25).to_dict(orient='records')

    return json.dumps([{
        'id': track['id'],
        'name': track['name'],
    } for track in playlist])


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

    return '''<script type="text/javascript">
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
      return String(Object.hasOwnProperty).replace('hasOwnProperty', 'postMessage');
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
</script>''' % user_id


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
