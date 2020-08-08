from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, bindparam
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func
from sqlalchemy.ext.declarative import declarative_base
from coolname import generate_slug
import sqlalchemy as sql
import psycopg2
import datetime
import creds

SERVER = 'localhost:5432'
DATABASE = 'UserTops'
USERNAME = 'postgres'
PASSWORD = creds.PASSWORD
DATABASE_CONNECTION = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}'

class Database():
    # create DB connection string with user:pw@server/dbname
    engine = sql.create_engine(DATABASE_CONNECTION)

    def __init__(self):
        # establishes connection when this database class is created wherever used.
        self.connection = self.engine.connect()
        print("Database Instance created")

    def create_user(self, user_id, user_name, user_country, user_profile_pic, session):
        session.add(Users(user_id=user_id, display_name=user_name, country=user_country, profile_picture=user_profile_pic))
    
    def update_login_time(self, user_id, session):
        user = session.query(Users).filter(Users.user_id == user_id).first()
        user.last_login = datetime.datetime.utcnow()

    def user_exists_in_table(self, user_id, table, session):
        return len(session.query(table).filter(table.user_id == user_id).all()) > 0

    def display_user_data(self, user_id, table, session):
        result = session.query(table).filter(table.user_id == user_id)
        for row in result:
            print ("rank:",row.rank, "URI: ",row.spotify_uri)
            
    def fetch_all_users_in_table(self, table, session):
        users = session.query(table).all()
        for user in users:
            print(user)

    def bulk_save_data(self, entries, session):
        session.bulk_save_objects(entries)

    def delete_user_data(self, user_id, table, session):
        result = session.query(table).filter(table.user_id == user_id)
        result.delete()

    def update_user_data(self, entries, table, session): 
        statement = table.__table__.update().where(table.user_id == bindparam('b_user_id')).where(table.rank == bindparam('b_rank')).values(spotify_uri=bindparam('b_spotify_uri'))
        session.execute(statement, entries)

    def save_user_tops(self, user_id, tracks_list, artists_list, session):
        # dummy_list = ['asdfadsfasdfasdf' for _ in range(50)]
        track_objects = []
        artist_objects = []
        for i in range(len(tracks_list)):
            track_item = tracks_list[i]
            track_uri = 'spotify:track:' + track_item['id']
            # track_uri = dummy_list[i]
            track_objects.append(TopTracks(user_id=user_id, spotify_uri=track_uri, rank=i))

            artist_item = artists_list[i]
            artist_uri = 'spotify:artist:' + artist_item['id']
            # artist_uri = dummy_list[i]
            artist_objects.append(TopArtists(user_id=user_id, spotify_uri=artist_uri, rank=i))      
        self.bulk_save_data(track_objects, session)
        self.bulk_save_data(artist_objects, session)
        
    def update_user_tops(self, user_id, tracks_list, artists_list, session):
        self.saveUserData(track_objects, session)
        self.saveUserData(artist_objects, session)
        updated_tracks = []
        updated_artists = []
        for i in range(len(tracks_list)):
            track_item = tracks_list[i]
            track_uri = 'spotify:track:' + track_item['id']
            updated_tracks.append({'b_user_id': user_id, 'b_spotify_uri': track_uri, 'b_rank': i})

            artist_item = artists_list[i]
            artist_uri = 'spotify:artist:' + artist_item['id']
            updated_artists.append({'b_user_id': user_id, 'b_spotify_uri': artist_uri, 'b_rank': i})
        
        self.update_user_data(updated_tracks, TopTracks, session)
        self.update_user_data(updated_artists, TopArtists, session)

    def get_shared(self, user_list, table, session):  # RANKSUM BABYYYY
        """
        Returns list of shared objects between n users.

        Parameters:
            user_list: list of user ids
            table: Track or Artist

        Returns:
            List containing lists of spotify uris and individual ranks sorted by their sum
        """
        user_data = [] # list of queries
        for user_id in user_list:
            user_data.append(session.query(table).filter(table.user_id == user_id))
        shared_data = {}
        for user in user_data:
            for row in user:
                uri = row.spotify_uri
                rank = row.rank
                if uri not in shared_data:
                    shared_data[uri] = [rank]
                else:
                    shared_data[uri].append(rank)

        for uri in shared_data:
            missing = len(user_list) - len(shared_data[uri])
            shared_data[uri] += [100] * missing

        ordered_data = [[uri, ranks] for uri, ranks in sorted(shared_data.items(), key=lambda item: sum(item[1]))]
        # print(ordered_data)
        return ordered_data

    def get_k_seeds(self, shared_data, k):
        # Returns first k spotify uris in shared data list
        return [item[0] for item in shared_data[:k]]
    
    def add_to_party(self, user_id, party_id, session):
        party_id, host, date_created = session.query(Party.party_id, Party.host, Party.date_created).filter(Party.party_id == party_id).first()
        session.add(Party(party_id=party_id, host=host, user_id=user_id, date_created=date_created))
    
    def create_party(self, user_id, session):
        session.add(Party(host=user_id, user_id=user_id))
    
    def get_party_users(self, party_id, session):
        row = session.query(Party.user_id).filter(Party.party_id == party_id).all()
        party_users = [user.user_id for user in row]
        return party_users

    def update_party_tracks(self, entries, session): 
        statement = PartyTracks.__table__.update().where(PartyTracks.party_id == bindparam('b_party_id')).where(PartyTracks.track_number == bindparam('b_track_number')).values(track_id=bindparam('b_track_id'))
        session.execute(statement, entries)

    def party_id_exists_in_table(self, party_id, table, session):
        return len(session.query(table).filter(table.party_id == party_id).all()) > 0

    def delete_party_data(self, party_id, table, session):
        result = session.query(table).filter(table.party_id == party_id)
        result.delete()

    def get_party_tracks(self, party_id, session):
        row = session.query(PartyTracks.track_id).filter(PartyTracks.party_id == party_id).all()
        party_tracks = [track.track_id for track in row]
        return party_tracks
    
    def user_exists_in_party(self, user_id, party_id, session):
        return len(session.query(Party).filter(Party.user_id == user_id, Party.party_id == party_id).all()) > 0

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    t_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    display_name = Column(String)
    country = Column(String)
    profile_picture = Column(String)
    account_created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)
    # invite_code = Column(String,  default=lambda: str(uuid.uuid4()), unique=True)

    def __repr__(self):
        return "<User(user_id='%s', display_name='%s', country='%s', profile_picture='%s')>" % (self.user_id, self.display_name, self.country, self.profile_picture)

class TopArtists(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    spotify_uri = Column(String)
    rank = Column(Integer)

    def __repr__(self):
        return "<Artist(user_id='%s', spotify_uri='%s', rank='%s')>" % (self.user_id, self.spotify_uri, self.rank)

class TopTracks(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    spotify_uri = Column(String)
    rank = Column(Integer)

    def __repr__(self):
        return "<Track(user_id='%s', spotify_uri='%s', rank='%s')>" % (self.user_id, self.spotify_uri, self.rank)

class Party(Base):
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True)
    party_id = Column(String, default=generate_slug(3))
    host = Column(Integer) # user_id, host privileges: deleting party, kick members, invite members
    user_id = Column(Integer)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    date_joined = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Party(party_id='%s', host='%s', user_id='%s', date_created='%s', date_joined='%s')>" % (self.party_id, self.host, self.user_id, self.date_created, self.date_joined)
        
class PartyTracks(Base):
    __tablename__ = 'party_tracks'
    id = Column(Integer, primary_key=True)
    party_id = Column(String)
    track_id = Column(String)
    track_number = Column(Integer)
    date_saved = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<PartyTrack(party_id='%s', track_id='%s', track_number='%s')>" % (self.party_id, self.track_id, self.track_number)
