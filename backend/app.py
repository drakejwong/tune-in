from getUserTops import getTops
from createPlaylist import generate
from spot_auth import user_id

topTracks, topArtists = getTops('short_term')

to_playlist = []

print("My Top Tracks")
for i, item in enumerate(topTracks):
    print(i+1, item['name'], '//', item['artists'][0]['name'])
    to_playlist.append(item['id'])

print("\nMy Top Artists")
for i, item in enumerate(topArtists):
    print(i+1, item['name'])

recs_list = generate("API Playlist Generation Test", to_playlist)
