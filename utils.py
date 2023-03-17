import pandas as pd
import spotipy
import random
import numpy as np
from sklearn.cluster import KMeans
from config import settings



date_range=pd.date_range(start=settings["Time"].start_date, end=settings["Time"].end_date)


def filter_albums(album_list):
    album_ids=[]
    album_names=[] 
    for album in album_list:
        if str(pd.to_datetime(album["added_at"]).date()) in date_range :
            album_ids.append(album["album"]["id"])
            album_names.append(album["album"]["name"])
    
    return album_ids
    

def filter_tracks(track_list):
    track_ids=[]
    track_names=[]
    for track in track_list:
        if str(pd.to_datetime(track["added_at"]).date()) in date_range :
            track_ids.append(track["track"]["id"])
            track_names.append(track["track"]["name"])
    return track_ids

def get_saved_albums(current_account):
    current_top_albums=[]
    while(True):
        fetched=current_account.current_user_saved_albums(offset=len(current_top_albums),limit=50)["items"]
        current_top_albums.extend(fetched)
        if len(fetched) < 50 : break
    return current_top_albums

def get_saved_tracks(current_account):
    current_top_tracks=[]
    while(True):
        fetched=current_account.current_user_saved_tracks(offset=len(current_top_tracks),limit=50)["items"]
        current_top_tracks.extend(fetched)
        if len(fetched) < 50 : break
    return current_top_tracks

def merge_tracks(current_account,album_ids,track_ids):
    for album in album_ids:
        track_ids.extend(list(map(lambda x:x.get("id"),current_account.album_tracks(album)["items"])))
        #track_names.extend(list(map(lambda x:x.get("name"),current_account.album_tracks(album)["items"])))
    return track_ids

def get_recommended_tracks(current_account,track_ids,num_of_tracks,**kwargs):
    recommendation_ids=[]
    recommendation_names=[]
    for _ in range(int(num_of_tracks/5)):
        sample_rec=current_account.recommendations(seed_tracks=random.sample(track_ids,5),limit=5,**kwargs)["tracks"]
        recommendation_ids.extend(list(map(lambda x:x.get("id"),sample_rec)))
        recommendation_names.extend(list(map(lambda x:x.get("name"),sample_rec)))
    return recommendation_ids,recommendation_names

def cluster_user_audio(current_account,track_ids):
    selection=["danceability","energy","speechiness","acousticness","instrumentalness","liveness"]
    features=current_account.audio_features(track_ids)
    filtered_selection=[f.get(s) for f in features for s in selection]
    filtered_selection=np.array(filtered_selection).reshape(int(len(filtered_selection)/len(selection)),len(selection))
    filtered_selection
    kmeans = KMeans(n_clusters=3, random_state=0).fit(filtered_selection)

