import spotipy
from spotipy.oauth2 import SpotifyOAuth
import creds

SPOTIPY_REDIRECT_URI="http://localhost:5000/callback/"

CACHE = ".userinfo"
scope = 'playlist-modify-public user-read-email user-top-read' #user-follow-read

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(creds.SPOTIPY_CLIENT_ID, creds.SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=CACHE))
# print(sp.me())
user_id = sp.me()['id']
user_name = sp.me()['display_name']
user_profile_pic = sp.me()['images'][0]['url'] if not '' else 'https://www.uokpl.rs/fpng/d/490-4909214_swag-wooper-png.png'