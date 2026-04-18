"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import logging
from recommender import load_songs, agentic_recommend_workflow, self_critique_recommendations

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting music recommender simulation")
    try:
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

        recommendations = agentic_recommend_workflow(user_prefs, songs, k=5)

        print("\nTop Recommendations:\n")
        for i, rec in enumerate(recommendations, 1):
            song, score, explanation, confidence = rec
            reasons = explanation.split("; ")
            print(f"{i}. {song['title']}")
            print(f"   Score: {score:.2f}")
            print(f"   Confidence: {confidence:.2f}")
            print("   Reasons:")
            for reason in reasons:
                print(f"   - {reason}")
            print()

        # Self-critique
        critique = self_critique_recommendations(recommendations, user_prefs)
        print(f"\nSelf-Critique: {critique}")
        
        logger.info("Recommendations generated successfully")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise


if __name__ == "__main__":
    main()
