from spot_auth import sp, user_id

# Get a user's top tracks and top artists
def get_top_tracks(term):
    # items returned are paging objects of Artists / Tracks, indexed into items -- "an array of (track or artist) objects"
    # https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
    # max is 50
    topTracks = sp.current_user_top_tracks(limit=50, time_range=term)['items']
    return topTracks

def get_top_artists(term):
    topArtists = sp.current_user_top_artists(limit=50, time_range=term)['items']
    return topArtists

def get_genre_seeds():
    return sp.recommendation_genre_seeds()

#get recommendations for a user based on up to 5 seed values of artists, tracks, or genres
#Parameters:
#seed_artists - a list of artist IDs, URIs or URLs
#seed_tracks - a list of track IDs, URIs or URLs
#seed_genres - a list of genre names.
#limit - min:1, max:100, default:20
#Returns: recommendations response object with keys seeds and tracks with values recommendation seed objects and track objects (simplified)
def recommend_tracks(tracks, artists=None, genres=None, lim=20):
    return sp.recommendations(seed_artists=artists, seed_genres=genres, seed_tracks=tracks, limit=lim)

# Creates a playlist for a user
def generate_party_playlist(playlist_name, track_ids, user_id, playlist_desc):
    new_playlist = sp.user_playlist_create(user_id, playlist_name, description=playlist_desc)
    sp.user_playlist_add_tracks(user_id, new_playlist['id'], track_ids)
