import spotipy
from spotipy.oauth2 import SpotifyOAuth

'''
This function requires the following environment variables to be set:
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

See here for more info:
https://spotipy.readthedocs.io/en/latest/#authorization-code-flow
'''


def spotipy_init():
    scope = "user-library-read,user-library-modify,user-read-recently-played,user-top-read,user-read-playback-position,streaming,app-remote-control,user-read-playback-state,user-modify-playback-state,user-read-currently-playing,playlist-read-private,playlist-read-collaborative,playlist-modify-private,playlist-modify-public,user-follow-read,user-follow-modify"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp
