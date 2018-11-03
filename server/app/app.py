from flask import Blueprint, json, Response

bp = Blueprint('app', __name__)


@bp.route('/')
def index():
    return 'Hey this is working!'


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
