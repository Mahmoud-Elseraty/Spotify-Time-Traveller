import re
from collections import Counter


def norm(text):
    text = re.sub(r"[\(\[].*?[\)\]]|\s-\s.*$", "", text.lower())
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def track_key(name, artist):
    return f"{norm(artist)}|{norm(name)}"


def pick_seeds(tracks, max_seeds):
    """Favour artists that dominate the era; ties keep the most recently added first."""
    counts = Counter(t["artists"][0] for t in tracks if t["artists"])
    ordered = sorted(tracks, key=lambda t: t["added_at"], reverse=True)
    ordered.sort(key=lambda t: counts.get(t["artists"][0] if t["artists"] else "", 0), reverse=True)
    seeds, seen_keys = [], set()
    for t in ordered:
        key = track_key(t["name"], t["artists"][0] if t["artists"] else "")
        if key not in seen_keys:
            seen_keys.add(key)
            seeds.append(t)
        if len(seeds) >= max_seeds:
            break
    return seeds, counts


def rank_candidates(seeds, artist_counts, provider, per_seed=20, on_progress=None):
    """Aggregate provider matches over all seeds: score = sum(seed weight * match)."""
    pool = {}
    for i, seed in enumerate(seeds):
        weight = artist_counts.get(seed["artists"][0], 1) if seed["artists"] else 1
        for cand in provider.similar(seed, limit=per_seed):
            entry = pool.setdefault(
                track_key(cand["name"], cand["artist"]),
                {"name": cand["name"], "artist": cand["artist"], "score": 0.0, "hits": 0},
            )
            entry["score"] += weight * cand["score"]
            entry["hits"] += 1
        if on_progress:
            on_progress(i + 1, len(seeds))
    ranked = sorted(pool.values(), key=lambda c: (c["score"], c["hits"]), reverse=True)
    top = ranked[0]["score"] if ranked else 1
    for c in ranked:
        c["match"] = c["score"] / top if top else 0
    return ranked


def select(ranked, resolve, exclude_ids, exclude_keys, count, max_per_artist):
    """Walk the ranking, resolve to Spotify tracks, drop seeds/library/duplicates, cap per artist."""
    out, seen_ids, per_artist = [], set(exclude_ids), Counter()
    seen_keys = set(exclude_keys)
    for cand in ranked:
        if len(out) >= count:
            break
        key = track_key(cand["name"], cand["artist"])
        if key in seen_keys:
            continue
        track = resolve(cand)
        if not track or track["id"] in seen_ids:
            continue
        primary = track["artist_ids"][0] if track["artist_ids"] else track["artists"][0]
        if max_per_artist and per_artist[primary] >= max_per_artist:
            continue
        seen_ids.add(track["id"])
        seen_keys.add(key)
        per_artist[primary] += 1
        out.append(dict(track, match=cand["match"]))
    return out
