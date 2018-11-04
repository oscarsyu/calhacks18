from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import six

from thesaurus import Word

import pprint
import sys

import spotipy
import spotipy.util as util

SPOTIPY_CLIENT_ID = "c57ae0a3f9b84353a57b9953201fc9c9"
SPOTIPY_CLIENT_SECRET = "94eaa60830c444c9a1b177f99b0fec1e"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"

def mood_dict():
    """ Gives a dictionary of mood synonyms. """
    happy_synonyms = Word("happy").synonyms() + ["happy"]
    sad_synonyms = Word("sad").synonyms() + ["sad"]
    excited_synonyms = Word("excited").synonyms() + ["excited"]
    calm_synonyms = Word("calm").synonyms() + ["calm"]
    moods = {
        "happy" : happy_synonyms,
        "sad" : sad_synonyms,
        "excited" : excited_synonyms,
        "calm" : calm_synonyms
    }
    return moods

def get_all_songs(username, maxi=200):
    scope = 'user-library-read'
    token = util.prompt_for_user_token(username, scope, \
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, \
        redirect_uri=SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    offset = 0
    result = []
    curr = sp.current_user_saved_tracks(offset=offset)
    while len([x["track"] for x in curr["items"]]) > 0 and len(result) <= maxi:
        for item in curr["items"]:
            result.append(item["track"])
        offset += 20
        curr = sp.current_user_saved_tracks(offset=offset)
    return result

def get_audio_features(username, tracks):
    """ Returns audio features. """
    scope = 'user-library-read'
    token = util.prompt_for_user_token(username, scope, \
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, \
        redirect_uri=SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    tracks = [t["uri"] for t in tracks]
    tracks = [tracks[i * 50:(i + 1) * 50] for i in range((len(tracks) +  49) // 50 )]  
    result = []
    for item in tracks:
        result.extend(sp.audio_features(item))
    return result

def make_playlist(username, tracks, name):
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, \
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, \
        redirect_uri=SPOTIPY_REDIRECT_URI)
    sp = spotipy.Spotify(auth=token)
    playlist = sp.user_playlist_create(username, name)
    tracks = [t["uri"] for t in tracks]
    tracks = [tracks[i * 100:(i + 1) * 100] for i in range((len(tracks) +  99) // 100 )]
    for item in tracks:
        sp.user_playlist_add_tracks(username, playlist["id"], item)  
    print('did it')


def main():

    if len(sys.argv) > 1:
        username = sys.argv[1]
        songs = get_all_songs(username, 2000)
        songs = [s for s in songs if s["artists"][0]["name"] == "Ariana Grande"]
        make_playlist(username, songs, "Ariana Grande Playlist")
    else:
        print("Usage: entity.py [username]")
        sys.exit()
    



if __name__ == '__main__': main()