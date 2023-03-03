import tomli
from login import *
from utils import *
def main(): 
    with open(".secrets.toml",mode="rb") as fp:
        credintials=tomli.load(fp)
    with open("settings.toml",mode="rb") as fpn:
        config=tomli.load(fpn)
    sp=get_access(credintials["Auth"])
    tracks=filter_tracks(get_saved_tracks(sp))
    albums=filter_albums(get_saved_albums(sp))
    tracks=merge_tracks(sp,albums,tracks)
    recommendations_ids,recommendations_name=get_recommended_tracks(sp,tracks,config["Playlist"].get("num_of_tracks"))

if(__name__=="__main__"):
    main()
