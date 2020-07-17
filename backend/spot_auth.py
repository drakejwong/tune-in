import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID="7c37dc9f80124866a7549d6128f0b9c2"
SPOTIPY_CLIENT_SECRET="8121a1f64d2947e09c8ac711d396f15a"
SPOTIPY_REDIRECT_URI="http://localhost:8888/callback/"

CACHE = ".cache-" + "test"
scope = 'playlist-modify-public user-read-email user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=CACHE))
user_id = sp.me()['id']
# user_id = 1263126600 #david id
# user_id = 1247633538 #vin id
