from spot_auth import sp, user_id

ITEM_LIMIT = 50

def get_top_tracks(term, limit=ITEM_LIMIT):
    # Returns array of track objects"
    # https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
    topTracks = sp.current_user_top_tracks(limit, time_range=term)['items']
    return topTracks

def get_top_tracks_all_terms(limit=ITEM_LIMIT):
    terms = ['short_term', 'medium_term', 'long_term']
    return [get_top_tracks(term) for term in terms]

# print(get_top_tracks('short_term')[1])

def get_top_artists(term, limit=ITEM_LIMIT):
    # Returns array of artist objects
    topArtists = sp.current_user_top_artists(limit, time_range=term)['items']
    return topArtists

def get_top_artists_all_terms(limit=ITEM_LIMIT):
    # Returns a nested list where each inner list has 50 top tracks from its term
    terms = ['short_term', 'medium_term', 'long_term']
    return [get_top_artists(term) for term in terms]

# def get_followed_artists(limit=ITEM_LIMIT):
#     artists = sp.current_user_followed_artists(limit)['artists']['items']

def recommend_tracks(tracks, artists=None, genres=None, lim=ITEM_LIMIT):
#get recommendations for a user based on up to 5 seed values of artists, tracks, or genres
#Parameters:
#   - seed values can be a list of uri's, url's, or id's
#   - limit - min:1, max:100, default:20
#Returns: recommendations object with keys seeds and tracks with values recommendation seed objects and track objects (simplified)
    return sp.recommendations(seed_artists=artists, seed_genres=genres, seed_tracks=tracks, limit=lim)

# Creates a playlist for a user
def generate_party_playlist(playlist_name, track_ids, user_id, playlist_desc):
    new_playlist = sp.user_playlist_create(user_id, playlist_name, description=playlist_desc)
    sp.user_playlist_add_tracks(user_id, new_playlist['id'], track_ids)
