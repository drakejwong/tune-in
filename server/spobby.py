from getUserTops import getTops
from createPlaylist import generate
from spot_auth import user_id
from getRecs import recommendTracks
# from algos import uri_conversion

def main():
    term = 'short_term'

    topTracks, topArtists = getTops(term)
    s_tracks = []
    s_artists = []

    print("My Top Tracks")
    for i, item in enumerate(topTracks):
        print(i+1, item['name'], '//', item['artists'][0]['name'])
        if i < 2:
            s_tracks.append('spotify:track:' + item['id'])

    print()
    print("My Top Artists")
    for i, item in enumerate(topArtists):
        print(i+1, item['name'])
        if i < 3:
            s_artists.append('spotify:artist:' + item['id'])

    results = recommendTracks(tracks=s_tracks, artists=s_artists)
    # results = recommendTracks(tracks=to_playlist)
    for r in results['tracks']:
        print("recommendation:", r['name'], "by", r['artists'][0]['name'])

    if results:
        recs = [track['id'] for track in results['tracks']]
        recs_list = generate("API Playlist Test", recs)

if __name__ == '__main__':
    main()
