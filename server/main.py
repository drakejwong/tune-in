import flask
from flask import request
from spot_auth import user_id, user_name, user_profile_pic
from spot_calls import get_top_tracks, get_top_tracks_all_terms, get_top_artists_all_terms, get_top_artists, recommend_tracks, generate_party_playlist
from database import Database, TopTracks, TopArtists, Users, Party, PartyTracks
from sqlalchemy.orm import Session
from contextlib import contextmanager

app = flask.Flask("__main__")

top_tracks_all_terms = get_top_tracks_all_terms()
top_artists_all_terms = get_top_artists_all_terms()

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
# party_id = 'able-shrewd-sunfish'
# with session_scope(db) as session:
#     db.grant_host(user_id, party_id, session)

#     db.create_party(696969, session)
    # db.delete_user_from_database(user_id, session)
    # db.delete_user_data(user_id, Users, session)
    # db.delete_user_data(user_id, TopTracks, session)
    # db.delete_user_data(user_id, TopArtists, session)

@app.route("/")
def login_redirect():
    db = Database()
    with session_scope(db) as session:
        update_user_data(db, session)
    namez = [tt["name"] + ' - ' + tt['artists'][0]["name"] for term in top_tracks_all_terms for tt in term]
    artz = [ta["name"] for term in top_artists_all_terms for ta in term]
    return flask.render_template("index.html", trax=namez, art=artz)

@app.route("/party/<party_id>") # we provide invite link, which is unique to every party
def party_invite(party_id):
    db = Database()
    with session_scope(db) as session:
        update_user_data(db, session)
        if not db.user_exists_in_party(user_id, party_id, session):
            db.add_to_party(user_id, party_id, session)
    
    # on click
    results = preview_party_playlist()
    namez = [track["name"] + ' - ' + track['artists'][0]["name"] for track in results['tracks']]
    return flask.render_template("index.html", trax=namez)
    
    # save_party_playlist()
    # return 'issa party' # party page

def update_user_data(db, session):
    # user_id = '696969'
    if db.user_exists_in_table(user_id, Users, session):
        assert db.user_exists_in_table(user_id, TopTracks, session) and db.user_exists_in_table(user_id, TopArtists, session)
        db.update_login_time(user_id, session)
        db.save_user_tops(user_id, top_tracks_all_terms, top_artists_all_terms, session, update=True)
    else:
        db.create_user(user_id, user_name, user_profile_pic, session)
        db.save_user_tops(user_id, top_tracks_all_terms, top_artists_all_terms, session)

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
    return results
    # display proposed tracks on front-end here
    # print("Recommended tracks:")
    # for track in results['tracks']:
    #     print(track['name'], "by", track['artists'][0]['name'])

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

def leave_party(): # on click
    party_id = fetch_party_id_from_url()
    db = Database()
    with session_scope(db) as session:
        if db.is_host(user_id, party_id, session):
            # if no one else is in party, delete party (db.delete_party_data())
            if len(db.get_party_users(party_id, session)) == 1:
                print('yeehaw')
                db.delete_party_data(party_id, session)
            else:
                db.delete_user_from_party(user_id, party_id, session)
                new_host = db.get_party_users(party_id, session)[0]
                db.grant_host(new_host, party_id, session)
        else:
            db.delete_user_from_party(user_id, party_id, session)
    # redirect to homepage or party directory

app.run(debug=True)
