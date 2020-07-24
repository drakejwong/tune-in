import flask
from getUserTops import getTops
from createPlaylist import generate
from spot_auth import user_id
from getRecs import recommendTracks
from dbTops import Database, Artist, Track

app = flask.Flask("__main__")

@app.route("/")
def login_redirect():
    term = 'short_term'

    topTracks, topArtists = getTops(term)
    # s_tracks = []
    # s_artists = []

    db = Database()

    for i, item in enumerate(topTracks):
        uripapa = 'spotify:track:' + item['id']
        # if i < 2:
        #     s_tracks.append(uripapa)
        db.saveData(Track(spotify_uri=uripapa, rank=i, user_id=user_id))

    for i, item in enumerate(topArtists):
        uripapa = 'spotify:artist:' + item['id']
        # if i < 3:
        #     s_artists.append(uripapa)
        db.saveData(Artist(spotify_uri=uripapa, rank=i, user_id=user_id))


    # results = recommendTracks(tracks=s_tracks, artists=s_artists)
    # results = recommendTracks(tracks=to_playlist)
    # for r in results['tracks']:
        # print("recommendation:", r['name'], "by", r['artists'][0]['name'])

    # if results:
    #     recs = [track['id'] for track in results['tracks']]
    #     recs_list = generate("API Playlist Test", recs)

    namez = [tt["name"] for tt in topTracks]
    artz = [ta["name"] for ta in topArtists]
    return flask.render_template("index.html", trax=namez, art=artz)

app.run(debug=True)
