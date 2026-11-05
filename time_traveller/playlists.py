def create_playlist(sp, name, description, track_uris, public=False):
    playlist = sp.current_user_playlist_create(name, public=public, description=description)
    for i in range(0, len(track_uris), 100):
        sp.playlist_add_items(playlist["id"], track_uris[i:i + 100])
    return playlist["external_urls"]["spotify"]
