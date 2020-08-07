import spotipy
from spotipy.oauth2 import SpotifyOAuth
import creds

SPOTIPY_REDIRECT_URI="http://localhost:5000/callback/"

CACHE = ".userinfo"
scope = 'playlist-modify-public user-read-email user-top-read'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(creds.SPOTIPY_CLIENT_ID, creds.SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=scope, cache_path=CACHE))
user_id = sp.me()['id']
user_country = sp.me()['country']
user_name = sp.me()['display_name']
pfp = sp.me()['images']
# print(len(pfp))
if not pfp:
    user_profile_pic = "https://www.uokpl.rs/fpng/d/490-4909214_swag-wooper-png.png"
else:
    user_profile_pic = sp.me()['images'][0]['url']
# print(user_profile_pic)
# user_profile_pic = "https://l.messenger.com/l.php?u=https%3A%2F%2Fscontent-atl3-1.xx.fbcdn.net%2Fv%2Ft1.0-1%2Fp320x320%2F93361290_1968136653331138_5810326840014798848_o.jpg%3F_nc_cat%3D111%26_nc_sid%3D0c64ff%26_nc_ohc%3DIIMmzs3L0x4AX9EsIKa%26_nc_ht%3Dscontent-atl3-1.xx%26_nc_tp%3D6%26oh%3D11ef8536fcd289091251aaf11cf1f417%26oe%3D5F530F14&h=AT3SqXydt90fkTmSC9rHnvWsP7kCB1ITwWe8WKT7HgxnA5_IXCAw-pSXChJUjBBsE_rvzszaJHn9HBHVa5LQtuhTTnRD2sT6jLjGnXSyjyJ64dzJIjtVrIVsdh77zCcV3db2yA"
