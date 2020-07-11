# Creates a playlist for a user

from spot_auth import sp, user_id

# scope = 'playlist-modify-public user-read-email user-top-read'

# parameters:
def generate(playlist_name, track_ids, friends_ids=None):
    recs = sp.user_playlist_create(user_id, playlist_name)
    playlist_id = recs["id"]
    sp.user_playlist_add_tracks(user_id, playlist_id, track_ids)
    # params: (playlist_owner_id, playlist_id)

    #API call -- Add the current authenticated user as a follower of a playlist.
    # if friends_ids:
    #     for f in friends_ids:
    #         sp.user_playlist_follow_playlist(user_id, f)
    return playlist_id
