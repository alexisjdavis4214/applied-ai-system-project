from src.recommender import Song, UserProfile, Recommender, recommend_songs, self_critique_recommendations
import pytest
import tempfile
import os

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_recommend_songs_with_confidence():
    """Test recommend_songs returns confidence scores."""
    songs = [
        {'id': 1, 'title': 'Song1', 'artist': 'Artist1', 'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'tempo_bpm': 120, 'valence': 0.9, 'danceability': 0.8, 'acousticness': 0.2},
        {'id': 2, 'title': 'Song2', 'artist': 'Artist2', 'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'tempo_bpm': 80, 'valence': 0.6, 'danceability': 0.5, 'acousticness': 0.9}
    ]
    user_prefs = {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.4}

    recs = recommend_songs(user_prefs, songs, k=2)
    assert len(recs) == 2
    for song, score, expl, conf in recs:
        assert isinstance(conf, float)
        assert 0 <= conf <= 1


def test_self_critique_recommendations():
    """Test self-critique function."""
    recommendations = [
        ({'genre': 'lofi', 'mood': 'chill'}, 3.0, "reasons", 0.8),
        ({'genre': 'pop', 'mood': 'happy'}, 2.0, "reasons", 0.5)
    ]
    user_prefs = {"favorite_genre": "lofi", "favorite_mood": "chill"}
    
    critique = self_critique_recommendations(recommendations, user_prefs)
    assert isinstance(critique, str)
    assert "confidence" in critique.lower()


def test_recommend_songs_consistency():
    """Test that recommend_songs gives consistent results for same input."""
    songs = [
        {'id': 1, 'title': 'Song1', 'artist': 'Artist1', 'genre': 'pop', 'mood': 'happy', 'energy': 0.8, 'tempo_bpm': 120, 'valence': 0.9, 'danceability': 0.8, 'acousticness': 0.2},
        {'id': 2, 'title': 'Song2', 'artist': 'Artist2', 'genre': 'lofi', 'mood': 'chill', 'energy': 0.4, 'tempo_bpm': 80, 'valence': 0.6, 'danceability': 0.5, 'acousticness': 0.9}
    ]
    user_prefs = {"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.4}

    # Run multiple times
    result1 = recommend_songs(user_prefs, songs, k=2)
    result2 = recommend_songs(user_prefs, songs, k=2)

    assert result1 == result2, "Recommendations should be consistent"


def test_recommend_songs_input_validation():
    """Test input validation in recommend_songs."""
    songs = [{'id': 1, 'title': 'Song1'}]  # Minimal song dict

    with pytest.raises(ValueError, match="user_prefs must be a dictionary"):
        recommend_songs("not a dict", songs)

    with pytest.raises(ValueError, match="songs must be a list of dictionaries"):
        recommend_songs({}, "not a list")

    with pytest.raises(ValueError, match="k must be a positive integer"):
        recommend_songs({}, songs, k=0)


def test_load_songs_error_handling():
    """Test error handling in load_songs."""
    with pytest.raises(FileNotFoundError):
        from src.recommender import load_songs
        load_songs("nonexistent.csv")

    # Create a temp file with invalid data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("id,title\ninvalid,valid\n")
        temp_path = f.name

    try:
        songs = load_songs(temp_path)
        assert len(songs) == 0  # Invalid row should be skipped
    finally:
        os.unlink(temp_path)
