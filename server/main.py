import flask
from flask import request
from getUserTops import get_top_tracks, get_top_artists
from createPlaylist import generate_party_playlist
from spot_auth import user_id, user_name, user_country, user_profile_pic
from getRecs import recommend_tracks
from database import Database, TopTracks, TopArtists, Users, Party, PartyTracks
from sqlalchemy.orm import Session
from contextlib import contextmanager

app = flask.Flask("__main__")

term = "short_term"
tracks_list = get_top_tracks(term)
artists_list = get_top_artists(term)

@contextmanager
def session_scope(db):
    """Provides a transactional scope around our session operations."""
    session = Session(bind=db.connection)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

# db = Database()
# with session_scope(db) as session:
#     db.delete_user_data(user_id, Party, session)

@app.route("/")
def login_redirect():
    db = Database()
    with session_scope(db) as session:
        update_user_data(db, session)
    namez = [tt["name"] for tt in tracks_list]
    artz = [ta["name"] for ta in artists_list]
    return flask.render_template("index.html", trax=namez, art=artz)

@app.route("/party/<party_id>") # we provide invite link, which is unique to every party
def party_invite(party_id):
    db = Database()
    with session_scope(db) as session:
        update_user_data(db, session)
        if not db.user_exists_in_party(user_id, party_id, session):
            print('we in here')
            db.add_to_party(user_id, party_id, session)
    # preview_party_playlist()
    # save_party_playlist()
    return 'issa party' # party page

def update_user_data(db, session):
    if db.user_exists_in_table(user_id, Users, session):
        db.update_login_time(user_id, session)
        db.update_user_tops(user_id, tracks_list, artists_list, session)
    else:
        db.create_user(user_id, user_name, user_country, user_profile_pic, session)
        db.save_user_tops(user_id, tracks_list, artists_list, session)

def preview_party_playlist(): 
    # on click, calculates seeds for users in party and displays recommended tracks, can be refreshed
    party_id = fetch_party_id_from_url() 
    db = Database()
    with session_scope(db) as session:
        party_users = db.get_party_users(party_id, session)
        shared_tracks = db.get_shared(party_users, TopTracks, session)
        shared_artists = db.get_shared(party_users, TopArtists, session)
        seed_tracks = db.get_k_seeds(shared_tracks, 3)
        seed_artists = db.get_k_seeds(shared_artists, 2)
        results = recommend_tracks(tracks=seed_tracks, artists=seed_artists)
        
        # save results to database
        if db.party_id_exists_in_table(party_id, PartyTracks, session):
            recommended_tracks = [{'b_party_id': party_id, 'b_track_id': track['id'], 'b_track_number': i} for i, track in enumerate(results['tracks'])]
            db.update_party_tracks(recommended_tracks, session)
        else:
            recommended_tracks = [PartyTracks(party_id=party_id, track_id=track['id'], track_number=i) for i, track in enumerate(results['tracks'])]
            db.bulk_save_data(recommended_tracks, session)

    # display proposed tracks on front-end here
    print("Recommended tracks:")
    for track in results['tracks']:
        print(track['name'], "by", track['artists'][0]['name'])

def save_party_playlist(): # button appears after displaying recommended tracks
    party_id = fetch_party_id_from_url()
    db = Database()
    with session_scope(db) as session:
        recommended_tracks = db.get_party_tracks(party_id, session)

    playlist_name = "it is PIZZATIME."
    playlist_desc = "ah sahhhhhhhhh düd"
    generate_party_playlist(playlist_name, recommended_tracks, user_id, playlist_desc)

def fetch_party_id_from_url():
    url = request.path
    tag = '/party/'
    party_id = url[url.index(tag) + len(tag) : len(url)]
    return party_id

app.run(debug=True)
