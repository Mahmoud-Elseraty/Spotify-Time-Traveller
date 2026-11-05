import json
import time

import requests

from ..config import ROOT

API = "https://ws.audioscrobbler.com/2.0/"
CACHE_PATH = ROOT / ".tt_cache" / "lastfm.json"


class LastFmProvider:
    """Similar-track lookup via Last.fm track.getSimilar (Spotify's recommendations API is closed to new apps)."""

    def __init__(self, api_key, session=None, cache_path=CACHE_PATH, delay=0.2):
        self.api_key = api_key
        self.session = session or requests.Session()
        self.cache_path = cache_path
        self.delay = delay
        self.cache = {}
        if cache_path and cache_path.exists():
            self.cache = json.loads(cache_path.read_text())

    def _save(self):
        if self.cache_path:
            self.cache_path.parent.mkdir(exist_ok=True)
            self.cache_path.write_text(json.dumps(self.cache))

    def similar(self, track, limit=20):
        """Return [{'name','artist','score'}] for a seed track dict (score in 0..1)."""
        artist = track["artists"][0] if track["artists"] else ""
        key = f"{artist.lower()}|{track['name'].lower()}|{limit}"
        if key not in self.cache:
            params = {
                "method": "track.getsimilar", "artist": artist, "track": track["name"],
                "limit": limit, "autocorrect": 1, "api_key": self.api_key, "format": "json",
            }
            resp = self.session.get(API, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("similartracks", {}).get("track", []) if "error" not in data else []
            self.cache[key] = [
                {"name": i["name"], "artist": i["artist"]["name"], "score": float(i.get("match") or 0)}
                for i in items
            ]
            time.sleep(self.delay)
        return self.cache[key]

    def close(self):
        self._save()
