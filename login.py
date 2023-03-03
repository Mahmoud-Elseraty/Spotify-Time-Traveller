import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_access(dict_credintials):
    auth_manager=SpotifyOAuth(**dict_credintials)
    sp=spotipy.Spotify(auth_manager=auth_manager)
    return sp

def create_playlists(current_account,names,descriptions,track_list):
    user=current_account.current_user()["id"]
    for name,description,counter in zip(names,descriptions,range(len(names))):
        start_index,end_index=((counter/len(names))*len(track_list),len(track_list)/len(names))
        playlist_id=current_account.user_playlist_create(user=user,name=name,public=False,description=description)["id"]
        current_account.user_playlist_add_tracks(user=user,playlist_id=playlist_id,tracks=track_list[int(start_index):int(end_index)])
        