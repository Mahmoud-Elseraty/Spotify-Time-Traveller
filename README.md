# Spotify-Time-Traveller
Travel back to the music you once listened to and find new songs similar to it.

## How it works
1. `pip install -r requirements.txt`
2. Copy `.secrets.toml.example` to `.secrets.toml` and fill in your Spotify app credentials and a free [Last.fm API key](https://www.last.fm/api/account/create). (`.secrets.toml` and `.cache` are git-ignored.)
3. Set the era and engine options in `settings.toml` (or pass flags).
4. Run:
   ```
   python main.py --from 07-2021 --to 01-2022 --count 30 [--name "My playlist"]
   ```
   Dates accept `MM-YYYY` or `YYYY-MM-DD`. Seeds come from liked songs, saved albums and your own playlists (by `added_at`); similar tracks are found through Last.fm, resolved on Spotify, and never include era tracks (or, by default, anything in your Liked Songs). With `--name` you are asked before a playlist is created.

Note: Spotify's recommendations/audio-features endpoints are unavailable to new apps, hence Last.fm for similarity.

## Tests
`python -m pytest`
