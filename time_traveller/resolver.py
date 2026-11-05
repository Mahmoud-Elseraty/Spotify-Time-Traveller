from .history import make_track


class SpotifyResolver:
    """Maps a (title, artist) candidate to a Spotify track via search."""

    def __init__(self, sp):
        self.sp = sp
        self.cache = {}

    def __call__(self, cand):
        key = (cand["name"].lower(), cand["artist"].lower())
        if key not in self.cache:
            q = f'track:"{cand["name"]}" artist:"{cand["artist"]}"'
            items = self.sp.search(q=q, type="track", limit=1)["tracks"]["items"]
            self.cache[key] = make_track(items[0], None, "candidate") if items else None
        return self.cache[key]
