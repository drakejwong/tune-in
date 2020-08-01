from database import Database, TopArtists, TopTracks
from getUserTops import getTops
from spot_auth import user_id

db = Database()

# db.fetchUserData(user_id, TopTracks, tracks_list)
# shared = db.getShared([user_id, 696969], TopArtists)
# db.getSeeds(shared, 5)
# print(db.userExistsInTable(696969, table=TopTracks))

# track_list = ['asdfadsfasdfasdf' for _ in range(50)]
# db.updateUserData(user_id, TopTracks, track_list)

# db.deleteUserData(user_id, TopTracks)
# db.deleteUserData(user_id, TopArtists)

# term = 'short_term'
# tracks_list, artists_list = getTops(term)

# if db.userExistsInTable(user_id, TopTracks):
#     print('User exists')
#     db.updateUserData(user_id, TopTracks, tracks_list)
# else:
#     for i, item in enumerate(tracks_list):
#         uripapa = 'spotify:track:' + item['id']
#         db.saveData(TopTracks(user_id=user_id, spotify_uri=uripapa, rank=i))

# if db.userExistsInTable(user_id, TopArtists):
#     db.updateUserData(user_id, TopArtists, artists_list)
# else:
#     for i, item in enumerate(artists_list):
#         uripapa = 'spotify:artist:' + item['id']
#         db.saveData(TopArtists(user_id=user_id, spotify_uri=uripapa, rank=i))