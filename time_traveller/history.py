from .dates import in_range


def _paginate(sp, page):
    while page:
        yield from page["items"]
        page = sp.next(page) if page.get("next") else None


def make_track(track, added_at, source):
    if not track or not track.get("id"):
        return None  # local files / removed tracks have no id
    return {
        "id": track["id"],
        "uri": track.get("uri") or f"spotify:track:{track['id']}",
        "name": track["name"],
        "artists": [a["name"] for a in track.get("artists", [])],
        "artist_ids": [a["id"] for a in track.get("artists", []) if a.get("id")],
        "added_at": added_at,
        "source": source,
    }


def get_liked_tracks(sp):
    out = []
    for item in _paginate(sp, sp.current_user_saved_tracks(limit=50)):
        t = make_track(item.get("track"), item["added_at"], "liked")
        if t:
            out.append(t)
    return out


def get_saved_album_tracks(sp, start, end):
    out = []
    for item in _paginate(sp, sp.current_user_saved_albums(limit=50)):
        if not in_range(item["added_at"], start, end):
            continue
        album = item["album"]
        for track in _paginate(sp, sp.album_tracks(album["id"], limit=50)):
            track = dict(track, album=album)
            t = make_track(track, item["added_at"], "album")
            if t:
                out.append(t)
    return out


def get_playlist_tracks(sp, start, end):
    me = sp.current_user()["id"]
    out = []
    for pl in _paginate(sp, sp.current_user_playlists(limit=50)):
        if (pl.get("owner") or {}).get("id") != me:
            continue
        for item in _paginate(sp, sp.playlist_items(pl["id"], limit=100)):
            if not item.get("added_at") or not in_range(item["added_at"], start, end):
                continue
            t = make_track(item.get("track") or item.get("item"), item["added_at"], "playlist")
            if t:
                out.append(t)
    return out


def dedupe_by_id(tracks):
    seen, out = set(), []
    for t in tracks:
        if t["id"] not in seen:
            seen.add(t["id"])
            out.append(t)
    return out


def get_era(sp, start, end, include_playlists=True):
    """Returns (seed tracks added in [start, end], all liked tracks for library exclusion)."""
    liked = get_liked_tracks(sp)
    seeds = [t for t in liked if in_range(t["added_at"], start, end)]
    seeds += get_saved_album_tracks(sp, start, end)
    if include_playlists:
        seeds += get_playlist_tracks(sp, start, end)
    return dedupe_by_id(seeds), liked
