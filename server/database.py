from sqlalchemy import MetaData, Table, Column, String, Integer, DateTime, bindparam
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, func
from sqlalchemy.ext.declarative import declarative_base
from coolname import generate_slug
import sqlalchemy as sql
import psycopg2
import datetime
import creds

SERVER = 'ec2-52-1-95-247.compute-1.amazonaws.com'
DATABASE = 'd5590mmicjpgm0'
USERNAME = 'bhjuosaogvrhfz'
PASSWORD = creds.PASSWORD
DATABASE_CONNECTION = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}'

class Database():
    # create DB connection string with user:pw@server/dbname
    engine = sql.create_engine(DATABASE_CONNECTION)

    def __init__(self):
        # establishes connection when this database class is created wherever used.
        self.connection = self.engine.connect()
        print("Database Instance created")

    def create_user(self, user_id, user_name, user_profile_pic, session):
        session.add(Users(user_id=user_id, display_name=user_name, profile_picture=user_profile_pic))
    
    def update_login_time(self, user_id, session):
        user = session.query(Users).filter(Users.user_id == user_id).first()
        user.last_login = datetime.datetime.utcnow()

    def user_exists_in_table(self, user_id, table, session):
        return len(session.query(table).filter(table.user_id == user_id).all()) > 0

    def bulk_save_data(self, entries, session):
        session.bulk_save_objects(entries)

    def delete_user_data(self, user_id, table, session):
        result = session.query(table).filter(table.user_id == user_id)
        result.delete()

    def update_user_data(self, entries, table, session): 
        statement = table.__table__.update().where(table.user_id == bindparam('b_user_id')).where(table.rank == bindparam('b_rank')).values(short_term=bindparam('b_short_term'), medium_term=bindparam('b_medium_term'), long_term=bindparam('b_long_term'))
        session.execute(statement, entries)
    
    # def delete_user_from_database(self, user_id, session):
    #     from sqlalchemy import MetaData
    #     m = MetaData()
    #     m.reflect(self.engine)
    #     for table in m.tables.values():
    #         self.delete_user_data(user_id, table, session)

    def save_user_tops(self, user_id, top_tracks_all_terms, top_artists_all_terms, session, update=False):
        num_terms = len(top_tracks_all_terms)
        #num_tracks_per_term = len(top_tracks_all_terms[0])
        assert num_terms == 3 #, num_tracks_per_term == 50
        
        track_objects = []
        artist_objects = []


        for i in range(50):
            
            ith_ranked_tracks_per_term = []
            ith_ranked_artists_per_term = []
            
            for term in range(num_terms):

                tracks_term = top_tracks_all_terms[term]
                if i < len(tracks_term):
                    track_item = tracks_term[i]
                    track_uri = track_item['uri']
                else: 
                    track_uri = "None"
                ith_ranked_tracks_per_term.append(track_uri)

                artists_term = top_artists_all_terms[term]
                if i < len(artists_term):
                    artist_item = artists_term[i]
                    artist_uri = artist_item['uri']
                else:
                    artist_uri = "None"
                ith_ranked_artists_per_term.append(artist_uri)
            
            if update:
                track_objects.append({'b_user_id': user_id, 'b_rank': i+1, 'b_short_term': ith_ranked_tracks_per_term[0], 'b_medium_term': ith_ranked_tracks_per_term[1], 'b_long_term': ith_ranked_tracks_per_term[2]})
                artist_objects.append({'b_user_id': user_id, 'b_rank': i+1, 'b_short_term': ith_ranked_artists_per_term[0], 'b_medium_term': ith_ranked_artists_per_term[1], 'b_long_term': ith_ranked_artists_per_term[2]})
            else:
                track_objects.append(TopTracks(user_id=user_id, rank=i+1, short_term=ith_ranked_tracks_per_term[0], medium_term=ith_ranked_tracks_per_term[1], long_term=ith_ranked_tracks_per_term[2]))
                artist_objects.append(TopArtists(user_id=user_id, rank=i+1, short_term=ith_ranked_artists_per_term[0], medium_term=ith_ranked_artists_per_term[1], long_term=ith_ranked_artists_per_term[2]))     

        if update:
            self.update_user_data(track_objects, TopTracks, session)
            self.update_user_data(artist_objects, TopArtists, session)
        else:
            self.bulk_save_data(track_objects, session)
            self.bulk_save_data(artist_objects, session)
        
    def get_shared(self, user_list, table, session):  # RANKSUM BABYYYY
        """
        Returns list of shared objects between n users.
-
        Parameters:
            user_list: list of user ids
            table: Track or Artist

        Returns:
            List containing lists of spotify uris and individual ranks sorted by their sum
        """
        user_data = [] # list of queries
        for user_id in user_list:
            user_data.append(session.query(table).filter(table.user_id == user_id))
        shared_data_dict = {}
        for user_query in user_data:
            for row in user_query:
                user_id = row.user_id
                rank = row.rank
                for track_in_term in [row.short_term, row.medium_term, row.long_term]:
                    if track_in_term in shared_data_dict and user_id not in shared_data_dict[track_in_term]: # only counts first instance of track in all terms for each user (skewed toward short term)
                        shared_data_dict[track_in_term][user_id] = rank
                    else:
                        shared_data_dict[track_in_term] = {user_id: rank}

        shared_data_list = []
        for uri, rank_dict in shared_data_dict.items():
            track = [uri, [rank for rank in rank_dict.values()]]
            missing = len(user_list) - len(track[1])
            track[1] += [100] * missing
            shared_data_list.append(track)
        
        ordered_data = sorted(shared_data_list, key=lambda item: sum(item[1]))
        # print(ordered_data)
        return ordered_data

    def get_k_seeds(self, shared_data, k):
        # Returns first k spotify uris in shared data list
        return [item[0] for item in shared_data[:k]]
    
    def add_to_party(self, user_id, party_id, session):
        party_id, host, date_created = session.query(Party.party_id, Party.host, Party.date_created).filter(Party.party_id == party_id).first()
        session.add(Party(party_id=party_id, host=host, user_id=user_id, date_created=date_created))
    
    def create_party(self, party_name, user_id, session):
        session.add(Party(party_id=party_name, host=user_id, user_id=user_id))
    
    def get_party_users(self, party_id, session):
        row = session.query(Party.user_id).filter(Party.party_id == party_id).all()
        party_users = [user.user_id for user in row]
        return party_users

    def update_party_tracks(self, entries, session): 
        statement = PartyTracks.__table__.update().where(PartyTracks.party_id == bindparam('b_party_id')).where(PartyTracks.track_number == bindparam('b_track_number')).values(track_id=bindparam('b_track_id'))
        session.execute(statement, entries)

    def party_id_exists_in_table(self, party_id, table, session):
        return len(session.query(table).filter(table.party_id == party_id).all()) > 0

    def delete_party_data(self, party_id, session):
        party = session.query(Party).filter(Party.party_id == party_id)
        party_tracks = session.query(PartyTracks).filter(PartyTracks.party_id == party_id)
        party.delete()
        party_tracks.delete()

    def get_party_tracks(self, party_id, session):
        row = session.query(PartyTracks.track_id).filter(PartyTracks.party_id == party_id).all()
        party_tracks = [track.track_id for track in row]
        return party_tracks
    
    def user_exists_in_party(self, user_id, party_id, session):
        return len(session.query(Party).filter(Party.user_id == user_id, Party.party_id == party_id).all()) > 0
    
    def is_host(self, user_id, party_id, session):
        return len(session.query(Party).filter(Party.host == user_id, Party.party_id == party_id).all()) > 0

    def delete_user_from_party(self, user_id, party_id, session):
        result = session.query(Party).filter(Party.user_id == user_id, Party.party_id == party_id)
        result.delete()
    
    def grant_host(self, user_id, party_id, session):
        party_rows = session.query(Party).filter(Party.party_id == party_id).all()
        for row in party_rows:
            row.host = user_id

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    t_id = Column(Integer, primary_key=True)
    user_id = Column(String)
    display_name = Column(String)
    profile_picture = Column(String)
    account_created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Users(user_id='%s', display_name='%s', profile_picture='%s')>" % (self.user_id, self.display_name, self.profile_picture)

class TopArtists(Base):
    __tablename__ = 'top_artists'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    rank = Column(Integer)
    short_term = Column(String)
    medium_term = Column(String)
    long_term = Column(String)

    def __repr__(self):
        return "<TopArtists(user_id='%s', rank='%s', short_term='%s', medium_term='%s', long_term='%s')>" % (self.user_id, self.rank, self.short_term, self.medium_term, self.long_term)

class TopTracks(Base):
    __tablename__ = 'top_tracks'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    rank = Column(Integer)
    short_term = Column(String)
    medium_term = Column(String)
    long_term = Column(String)

    def __repr__(self):
        return "<TopTracks(user_id='%s', rank='%s', short_term='%s', medium_term='%s', long_term='%s')>" % (self.user_id, self.rank, self.short_term, self.medium_term, self.long_term)

class Party(Base):
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True)
    party_id = Column(String)
    host = Column(String) # user_id, host privileges: deleting party, kick members, invite members
    user_id = Column(String)
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
        return "<PartyTracks(party_id='%s', track_id='%s', track_number='%s', date_saved='%s')>" % (self.party_id, self.track_id, self.track_number, self.date_saved)
