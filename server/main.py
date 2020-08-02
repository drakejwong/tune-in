import flask
from getUserTops import getTops
from createPlaylist import generate
from spot_auth import user_id, user_name, user_country, user_profile_pic
from getRecs import recommendTracks
from database import Database, TopTracks, TopArtists, Users
from sqlalchemy.orm import Session

app = flask.Flask("__main__")

@app.route("/")
def login_redirect():
    term = 'short_term'
    tracks_list, artists_list = getTops(term)
    assert len(tracks_list) == len(artists_list)    

    db = Database()
    session = Session(bind=db.connection)
    try:
        # db.deleteUserData(user_id, TopTracks, session)
        # db.deleteUserData(user_id, TopArtists, session)
        # db.deleteUserData(user_id, Users, session)
        
        if db.userExistsInTable(user_id, Users, session):
            db.updateLoginTime(user_id, session)
            db.updateUserTops(user_id, tracks_list, artists_list, session)
        else:
            db.createUser(user_id, user_name, user_country, user_profile_pic, session)
            db.saveUserTops(user_id, tracks_list, artists_list, session)

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

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
