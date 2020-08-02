from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, bindparam
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql
import psycopg2
import datetime
import creds

SERVER = 'localhost:5432'
DATABASE = 'test'
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

    def fetchByQuery(self, query):
        fetchQuery = self.connection.execute(f"SELECT * FROM {query}")
        for data in fetchQuery.fetchall():
            print(data)

    def createUser(self, user_id, user_name, user_country, user_profile_pic, session):
        session.add(Users(user_id=user_id, display_name=user_name, country=user_country, profile_picture=user_profile_pic))
    
    def updateLoginTime(self, user_id, session):
        user = session.query(Users).filter(Users.user_id == user_id).first()
        user.last_login = datetime.datetime.utcnow()

    def userExistsInTable(self, user_id, table, session):
        return len(session.query(table).filter(table.user_id == user_id).all()) > 0

    def displayUserData(self, user_id, table, session):
        result = session.query(table).filter(table.user_id == user_id)
        for row in result:
            print ("rank:",row.rank, "URI: ",row.spotify_uri)
    
    def fetchAllUsersInTable(self, table, session):
        users = session.query(table).all()
        for user in users:
            print(user)

    def saveUserData(self, entries, session):
        session.bulk_save_objects(entries)

    def deleteUserData(self, user_id, table, session):
        result = session.query(table).filter(table.user_id == user_id)
        result.delete()

    def updateUserData(self, entries, table, session): 
        statement = table.__table__.update().where(table.user_id == bindparam('b_user_id')).where(table.rank == bindparam('b_rank')).values(spotify_uri=bindparam('b_spotify_uri'))
        session.execute(statement, entries)

    def saveUserTops(self, user_id, tracks_list, artists_list, session):
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
      
        self.saveUserData(track_objects, session)
        self.saveUserData(artist_objects, session)
        
    def updateUserTops(self, user_id, tracks_list, artists_list, session):
        # dummy_list = ['asdfadsfasdfasdf' for _ in range(50)]
        updated_tracks = []
        updated_artists = []
        for i in range(len(tracks_list)):
            track_item = tracks_list[i]
            track_uri = 'spotify:track:' + track_item['id']
            # track_uri = dummy_list[i]
            updated_tracks.append({'b_user_id': user_id, 'b_spotify_uri': track_uri, 'b_rank': i})

            artist_item = artists_list[i]
            artist_uri = 'spotify:artist:' + artist_item['id']
            # artist_uri = dummy_list[i]
            updated_artists.append({'b_user_id': user_id, 'b_spotify_uri': artist_uri, 'b_rank': i})
        
        self.updateUserData(updated_tracks, TopTracks, session)
        self.updateUserData(updated_artists, TopArtists, session)

    def getShared(self, user_list, table, session):  # RANKSUM BABYYYY
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
        print(ordered_data)
        return ordered_data

    def getSeeds(self, shared_data, k):
        # Returns first k spotify uris in shared data list
        return [item[0] for item in shared_data[:k]]

Base = declarative_base()

class TopArtists(Base):
    """Model for top artists table."""
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    spotify_uri = Column(String)
    rank = Column(Integer)

    def __repr__(self):
        return "<Artist(user_id='%s', spotify_uri='%s', rank='%s')>" % (self.user_id, self.spotify_uri, self.rank)

class TopTracks(Base):
    """Model for top tracks table."""
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    spotify_uri = Column(String)
    rank = Column(Integer)

    def __repr__(self):
        return "<Track(user_id='%s', spotify_uri='%s', rank='%s')>" % (self.user_id, self.spotify_uri, self.rank)
        
class Users(Base):
    """Model for users table."""
    __tablename__ = 'users'
    t_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    display_name = Column(String)
    country = Column(String)
    profile_picture = Column(String)
    account_created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<User(user_id='%s', display_name='%s', country='%s', profile_picture='%s')>" % (self.user_id, self.display_name, self.country, self.profile_picture)