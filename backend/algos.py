#Panoramic Partners Proprietary "tune-in" Algorithm

#Paramter cmp_list: a list of user data objects (top artists / tracks tables) to compare
def rankSum(cmp_lst):
    ranked = []
    for user in cmp_lst:
        user["rank"]
    return ranked

#Convert a Spotify ID to a Spotify URI -- Parameters:
#id (string): Spotify ID
#type: 0, 1 (track, artist)
# def uri_conversion(id, type):
#     if type != 0 or type != 1:
#         print("Invalid")
#         return -1
#     if type == 0: uri = 'spotify:track:' + id
#     else: uri = 'spotify:artist:' + id
#     return uri
