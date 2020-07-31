from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
import psycopg2

SERVER = 'localhost:5432'
DATABASE = 'test'
USERNAME = 'postgres'
PASSWORD = 'dbisadbdev'
DATABASE_CONNECTION = f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}'

class Database():
    #create DB connection string with user:pw@server/dbname
    engine = db.create_engine(DATABASE_CONNECTION)

    def __init__(self):
        #establishes connection when this database class is created wherever used.
        self.connection = self.engine.connect()
        print("Database Instance created")

    def saveData(self, user):
        session = Session(bind=self.connection)
        session.add(user)
        session.commit()

    def fetchUserByName(self):
        meta = MetaData()
        user = Table('user', meta,
                        Column('name'),
                        Column('age'),
                        Column('email'),
                        Column('address'),
                        Column('zip_code'))
        data = self.connection.execute(user.select())
        for user in data:
            print(user)

    def fetchAllUsers(self):
        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)
        users = self.session.query(User).all()
        for user in users:
            print(user)

    def fetchByQuery(self, query):
        fetchQuery = self.connection.execute(f"SELECT * FROM {query}")

        for data in fetchQuery.fetchall():
            print(data)

    def updateUser(self, userName, address):
        session = Session(bind=self.connection)
        dataToUpdate = {User.address: address}
        userData = session.query(User).filter(User.name==userName)
        userData.update(dataToUpdate)
        session.commit()

    def deleteUser(self, user):
        session = Session(bind=self.connection)
        userData = session.query(User).filter(User.name==user).first()
        session.delete(userData)
        session.commit()

Base = declarative_base()

class User(Base):
    """Model for user information."""
    __tablename__ = 'users'
    name = Column(String)
    age = Column(Integer)
    email = Column(String)
    address = Column(String)
    zip_code = Column(String)
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return "<User(name='%s', age='%s', email='%s', address='%s', zip code='%s')>" % (self.name, self.age, self.email, self.address, self.zip_code)
