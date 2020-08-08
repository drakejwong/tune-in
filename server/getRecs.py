#get recommendations for a user based on up to 5 seed values of artists, tracks, or genres

from spot_auth import sp, user_id

def get_genre_seeds():
    return sp.recommendation_genre_seeds()

#Parameters:
#seed_artists - a list of artist IDs, URIs or URLs
#seed_tracks - a list of track IDs, URIs or URLs
#seed_genres - a list of genre names.
#limit - min:1, max:100, default:20
#Returns: recommendations response object with keys seeds and tracks with values recommendation seed objects and track objects (simplified)
def recommend_tracks(tracks, artists=None, genres=None, lim=20):
    return sp.recommendations(seed_artists=artists, seed_genres=genres, seed_tracks=tracks, limit=lim)

# def recommendTracks(tracks):
#     return sp.recommendations(seed_tracks=tracks)
# def recommendTracks(artists):
#     return sp.recommendations(seed_artists=artists)
