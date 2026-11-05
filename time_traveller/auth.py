import spotipy
from spotipy.oauth2 import SpotifyOAuth

from .config import ROOT


def get_access(credentials):
    auth_manager = SpotifyOAuth(cache_path=str(ROOT / ".cache"), **credentials)
    return spotipy.Spotify(auth_manager=auth_manager, retries=5, status_retries=5, backoff_factor=1)
