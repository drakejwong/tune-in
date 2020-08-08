# Creates a playlist for a user

from spot_auth import sp, user_id

def generate_party_playlist(playlist_name, track_ids, user_id, playlist_desc):
    new_playlist = sp.user_playlist_create(user_id, playlist_name, description=playlist_desc)
    sp.user_playlist_add_tracks(user_id, new_playlist['id'], track_ids)
    


    #API call -- Add the current authenticated user as a follower of a playlist.
    # params: (playlist_owner_id, playlist_id)
    # if friends_ids:
    #     for f in friends_ids:
    #         sp.user_playlist_follow_playlist(user_id, f)