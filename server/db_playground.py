from database import Database, TopArtists, TopTracks
from spot_auth import user_id

db = Database()

# shared = db.getShared([user_id, 696969], TopArtists)
# db.getSeeds(shared, 5)
# print(db.userExistsInTable(696969, table=TopTracks))

# track_list = ['asdfadsfasdfasdf' for _ in range(50)]
# db.updateUserTracks(123, track_list)

# db.deleteUserData(user_id, TopTracks)