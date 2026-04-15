from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV file."""
    songs = []
    with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness'])
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song based on user preferences."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song['genre'] == user_prefs.get('favorite_genre'):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0
    if song['mood'] == user_prefs.get('favorite_mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Numeric features
    features = [
        ('energy', 0.5, 'target_energy'),
        ('tempo_bpm', 0.4, 'target_tempo_bpm'),
        ('valence', 0.4, 'target_valence'),
        ('danceability', 0.4, 'target_danceability'),
        ('acousticness', 0.4, 'target_acousticness')
    ]

    for feature, weight, pref_key in features:
        if pref_key in user_prefs:
            user_val = user_prefs[pref_key]
            song_val = song[feature]
            if feature == 'tempo_bpm':
                # Normalize tempo difference by assuming max range of 200 BPM
                diff = abs(song_val - user_val) / 200
                similarity = max(0, 1 - diff)
            else:
                similarity = max(0, 1 - abs(song_val - user_val))
            feature_score = weight * similarity
            score += feature_score
            reasons.append(f"{feature} similarity ({similarity:.2f}) × {weight} = +{feature_score:.2f}")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Recommend top k songs based on user preferences."""
    # Score all songs using list comprehension (Pythonic way)
    scored_songs = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    
    # Sort by score descending (in-place sort)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k
    return scored_songs[:k]
