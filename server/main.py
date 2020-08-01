import flask
from getUserTops import getTops
from createPlaylist import generate
from spot_auth import user_id
from getRecs import recommendTracks
from database import Database, TopArtists, TopTracks

app = flask.Flask("__main__")

@app.route("/")
def login_redirect():
    term = 'short_term'
    tracks_list, artists_list = getTops(term)
    # dummy_list = ['asdfadsfasdfasdf' for _ in range(50)]
    assert len(tracks_list) == len(artists_list)
    N = len(tracks_list)
    
    db = Database()
    db.deleteUserData(user_id, TopTracks)
    db.deleteUserData(user_id, TopArtists)

    track_objects = artist_objects = []
    for i in range(N):
        track_item = tracks_list[i]
        track_uri = 'spotify:track:' + track_item['id']
        # track_uri = dummy_list[i]
        track_objects.append(TopTracks(user_id=user_id, spotify_uri=track_uri, rank=i))

        artist_item = artists_list[i]
        artist_uri = 'spotify:artist:' + artist_item['id']
        # artist_uri = dummy_list[i]
        artist_objects.append(TopArtists(user_id=user_id, spotify_uri=artist_uri, rank=i))
    
    db.saveUserData(track_objects)
    db.saveUserData(artist_objects)
    
    """
    DUDE THIS SHIT SHOULD WORK BUT IT DOESNT WTF
    if db.userExistsInTable(user_id, TopTracks) and db.userExistsInTable(user_id, TopArtists):
        # preparing to bulk update
        updated_tracks = updated_artists = []
        for i in range(N):
            track_item = tracks_list[i]
            track_uri = 'spotify:track:' + track_item['id']
            # track_uri = dummy_list[i]
            updated_tracks.append({'b_user_id': user_id, 'b_spotify_uri': track_uri, 'b_rank': i})

            artist_item = artists_list[i]
            artist_uri = 'spotify:artist:' + artist_item['id']
            # artist_uri = dummy_list[i]
            updated_artists.append({'b_user_id': user_id, 'b_spotify_uri': artist_uri, 'b_rank': i})
        
        db.updateUserData(updated_tracks, TopTracks)
        db.updateUserData(updated_artists, TopArtists)

    else:
        # preparing to bulk save
        track_objects = artist_objects = []
        for i in range(N):
            track_item = tracks_list[i]
            track_uri = 'spotify:track:' + track_item['id']
            track_objects.append(TopTracks(user_id=user_id, spotify_uri=track_uri, rank=i))

            artist_item = artists_list[i]
            artist_uri = 'spotify:artist:' + artist_item['id']
            artist_objects.append(TopArtists(user_id=user_id, spotify_uri=artist_uri, rank=i))
        
        db.saveUserData(track_objects)
        db.saveUserData(artist_objects)
    """
        

    # results = recommendTracks(tracks=s_tracks, artists=s_artists)
    # results = recommendTracks(tracks=to_playlist)
    # for r in results['tracks']:
        # print("recommendation:", r['name'], "by", r['artists'][0]['name'])

    # if results:
    #     recs = [track['id'] for track in results['tracks']]
    #     recs_list = generate("API Playlist Test", recs)

    namez = [tt["name"] for tt in tracks_list]
    artz = [ta["name"] for ta in artists_list]
    return flask.render_template("index.html", trax=namez, art=artz)

app.run(debug=True)
