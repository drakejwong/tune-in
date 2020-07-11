from getUserTops import getTops
from createPlaylist import generate
from spot_auth import user_id
from getRecs import recommendTracks

topTracks, topArtists = getTops('short_term')

to_playlist = []

print("My Top Tracks")
for i, item in enumerate(topTracks):
    # print(i+1, item['name'], '//', item['artists'][0]['name'])

    if i < 5:
        to_playlist.append('spotify:track:' + item['id'])

# print("\nMy Top Artists")
# for i, item in enumerate(topArtists):
#     print(i+1, item['name'])

results = recommendTracks(tracks=to_playlist)
# for r in recs['tracks']:
#     print("recommendation:", r['name'], "by", r['artists'][0]['name'])
recs = [track['id'] for track in results['tracks']]

recs_list = generate("API Playlist Recommendation Test", recs)
