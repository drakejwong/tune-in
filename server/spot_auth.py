import spotipy
from spotipy.oauth2 import SpotifyOAuth
# import creds

SPOTIPY_CLIENT_ID="e4e6d6d4631e4ed5b0b06975e16aba24"
SPOTIPY_CLIENT_SECRET="3d439b94b1724600895dcd6d5d016bb8"
SPOTIPY_REDIRECT_URI="http://localhost:5000/callback/"

CACHE = ".userinfo"
scope = 'playlist-modify-public user-read-email user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=CACHE))
user_id = sp.me()['id']
