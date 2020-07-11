# Get a user's top tracks and top artists
from spot_auth import sp, user_id

# terms = ['short_term', 'medium_term', 'long_term']
# term = 'short_term'


def getTops(term):
    # items returned are paging objects of Artists / Tracks, indexed into items -- "an array of (track or artist) objects"
    # https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/
    topTracks = sp.current_user_top_tracks(limit=50, time_range=term)['items']
    topArtists = sp.current_user_top_artists(limit=50, time_range=term)['items']
    return topTracks, topArtists
