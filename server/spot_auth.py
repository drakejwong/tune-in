import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID="f0175fcbf5dc47c8a909e0a75b76d8c3"
SPOTIPY_CLIENT_SECRET="08a915ee4ba545c89c5be5ccae464e9d"
SPOTIPY_REDIRECT_URI="http://localhost:5000/callback/"

CACHE = ".userinfo"
scope = 'playlist-modify-public user-read-email user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=CACHE))
user_id = sp.me()['id']
# user_id = 1263126600 #david id
# user_id = 1247633538 #vin id
