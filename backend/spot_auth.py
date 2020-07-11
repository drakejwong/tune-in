import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID="no"
SPOTIPY_CLIENT_SECRET="no"
SPOTIPY_REDIRECT_URI="http://localhost:8888/callback/"

CACHE = ".cache-" + "test"
scope = 'playlist-modify-public user-read-email user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=CACHE))
# user_id = sp.me()['id']
user_id = "nuh uh"
