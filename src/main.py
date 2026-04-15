"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_tempo_bpm": 78.0,
        "target_valence": 0.58,
        "target_danceability": 0.60,
        "target_acousticness": 0.78
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop Recommendations:\n")
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        reasons = explanation.split("; ")
        print(f"{i}. {song['title']}")
        print(f"   Score: {score:.2f}")
        print("   Reasons:")
        for reason in reasons:
            print(f"   - {reason}")
        print()


if __name__ == "__main__":
    main()
