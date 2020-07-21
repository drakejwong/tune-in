import flask
from getUserTops import getTops
from createPlaylist import generate
from spot_auth import user_id
from getRecs import recommendTracks


app = flask.Flask("__main__")

@app.route("/")
def my_index():
    return flask.render_template("index.html", myfuckinguy="we did it reddit")

@app.route("/callback/")
def login_redirect():
    # token = []
    # for l in literal.split("&"):
    #     token.append(l)
        # for var, tok in l.split("="):
        #     eval(f'{var}="{tok}"')
    term = 'short_term'

    topTracks, topArtists = getTops(term)
    s_tracks = []
    s_artists = []

    # print("My Top Tracks")
    for i, item in enumerate(topTracks):
        # print(i+1, item['name'], '//', item['artists'][0]['name'])
        if i < 2:
            s_tracks.append('spotify:track:' + item['id'])

    # print("\nMy Top Artists")
    for i, item in enumerate(topArtists):
        print(i+1, item)
        if i < 3:
            s_artists.append('spotify:artist:' + item['id'])

    results = recommendTracks(tracks=s_tracks, artists=s_artists)
    # results = recommendTracks(tracks=to_playlist)
    # for r in results['tracks']:
        # print("recommendation:", r['name'], "by", r['artists'][0]['name'])
    return flask.render_template("index.html", myfuckinguy=s_tracks, boi=s_artists)

app.run(debug=True)