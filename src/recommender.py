from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv
import logging
import json
import os

# Configure logging for reliability tracking
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    """Load songs from CSV file with error handling."""
    songs = []
    try:
        with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
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
                except (ValueError, KeyError) as e:
                    logger.warning(f"Skipping invalid song row: {row}. Error: {e}")
        logger.info(f"Loaded {len(songs)} songs from {csv_path}")
    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
        raise
    except Exception as e:
        logger.error(f"Error loading songs from {csv_path}: {e}")
        raise
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song based on user preferences with logging."""
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

    logger.debug(f"Scored song '{song['title']}' with score {score:.2f}")
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str, float]]:
    """Recommend top k songs based on user preferences with reliability checks and confidence scores."""
    if not isinstance(user_prefs, dict):
        raise ValueError("user_prefs must be a dictionary")
    if not isinstance(songs, list) or not all(isinstance(s, dict) for s in songs):
        raise ValueError("songs must be a list of dictionaries")
    if k <= 0:
        raise ValueError("k must be a positive integer")
    if not songs:
        logger.warning("No songs provided for recommendation")
        return []

    logger.info(f"Recommending top {k} songs for user preferences: {user_prefs}")

    # Score all songs using list comprehension (Pythonic way)
    scored_songs = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    
    # Sort by score descending (in-place sort)
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Calculate confidence: fraction of maximum possible score (2.0 genre + 1.0 mood + 2.1 features = 5.1)
    MAX_SCORE = 5.1
    top_k = scored_songs[:k]
    confidences = [min(1.0, score / MAX_SCORE) for _, score, _ in top_k]
    
    # Return with confidence
    result = [(song, score, expl, conf) for (song, score, expl), conf in zip(top_k, confidences)]
    logger.info(f"Recommended {len(result)} songs with confidence scores")
    return result


def retrieve_knowledge(user_prefs: Dict, knowledge_path: str = "data/knowledge.json") -> str:
    """RAG: Retrieve relevant knowledge from custom documents."""
    try:
        with open(knowledge_path, 'r') as f:
            knowledge = json.load(f)
        
        retrieved = []
        genre = user_prefs.get('favorite_genre')
        mood = user_prefs.get('favorite_mood')
        
        if genre and genre in knowledge.get('genres', {}):
            retrieved.append(f"Genre info: {knowledge['genres'][genre]}")
        
        if mood and mood in knowledge.get('moods', {}):
            retrieved.append(f"Mood info: {knowledge['moods'][mood]}")
        
        # Retrieve song-specific if available
        # For simplicity, retrieve all song knowledge
        
        return " ".join(retrieved) if retrieved else "No specific knowledge retrieved."
    except Exception as e:
        logger.warning(f"Failed to retrieve knowledge: {e}")
        return "Knowledge retrieval failed."


def self_critique_recommendations(recommendations: List[Tuple[Dict, float, str, float]], user_prefs: Dict) -> str:
    """Self-critique the recommendations for reliability and quality."""
    if not recommendations:
        return "No recommendations to critique."

    # Check average confidence
    avg_confidence = sum(conf for _, _, _, conf in recommendations) / len(recommendations)
    
    # Check if top recommendation matches key prefs
    top_song, _, _, _ = recommendations[0]
    matches_genre = top_song['genre'] == user_prefs.get('favorite_genre')
    matches_mood = top_song['mood'] == user_prefs.get('favorite_mood')
    
    critique = f"Average confidence: {avg_confidence:.2f}. "
    if avg_confidence > 0.7:
        critique += "High confidence in recommendations. "
    elif avg_confidence > 0.4:
        critique += "Moderate confidence. "
    else:
        critique += "Low confidence; consider refining preferences. "
    
    if matches_genre and matches_mood:
        critique += "Top recommendation strongly matches user preferences."
    elif matches_genre or matches_mood:
        critique += "Top recommendation partially matches user preferences."
    else:
        critique += "Top recommendation may not align well; review scoring logic."
    
    logger.info(f"Self-critique: {critique}")
    return critique


def agentic_recommend_workflow(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str, float]]:
    """Agentic Workflow: Multi-step reasoning with observable steps."""
    logger.info("Step 1: Analyzing user preferences")
    # Analyze prefs
    has_genre = 'favorite_genre' in user_prefs
    has_mood = 'favorite_mood' in user_prefs
    logger.info(f"Preferences analyzed: genre={has_genre}, mood={has_mood}")
    
    logger.info("Step 2: Retrieving knowledge")
    knowledge = retrieve_knowledge(user_prefs)
    logger.info(f"Knowledge retrieved: {len(knowledge)} chars")
    
    logger.info("Step 3: Scoring songs")
    scored_songs = [
        (song, score, "; ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    logger.info(f"Scored {len(scored_songs)} songs")
    
    logger.info("Step 4: Ranking and selecting top k")
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    top_k = scored_songs[:k]
    
    logger.info("Step 6: Calculating confidence")
    MAX_SCORE = 5.1
    confidences = [min(1.0, score / MAX_SCORE) for _, score, _ in top_k]
    
    result = [(song, score, expl, conf) for (song, score, expl), conf in zip(top_k, confidences)]
    logger.info("Step 7: Self-critique")
    critique = self_critique_recommendations(result, user_prefs)
    logger.info(f"Critique: {critique}")
    
    return result
