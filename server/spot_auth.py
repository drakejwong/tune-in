import spotipy
from spotipy.oauth2 import SpotifyOAuth
import creds

# SPOTIPY_CLIENT_ID=""
# SPOTIPY_CLIENT_SECRET=""
SPOTIPY_REDIRECT_URI="http://localhost:5000/callback/"

CACHE = ".userinfo"
scope = 'playlist-modify-public user-read-email user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(creds.SPOTIPY_CLIENT_ID, creds.SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=CACHE))
user_id = sp.me()['id']
