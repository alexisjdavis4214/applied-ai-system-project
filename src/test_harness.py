"""
Test Harness or Evaluation Script: Runs system on predefined inputs and prints summary.
"""

import logging
from recommender import load_songs, agentic_recommend_workflow, self_critique_recommendations

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_test_harness():
    """Test harness with predefined inputs."""
    logger.info("Starting test harness evaluation")
    
    try:
        songs = load_songs("data/songs.csv")
        
        test_cases = [
            {
                "name": "Lofi Chill User",
                "prefs": {
                    "favorite_genre": "lofi",
                    "favorite_mood": "chill",
                    "target_energy": 0.40,
                    "target_tempo_bpm": 78.0,
                    "target_valence": 0.58,
                    "target_danceability": 0.60,
                    "target_acousticness": 0.78
                },
                "expected_top_genre": "lofi"
            },
            {
                "name": "Pop Happy User",
                "prefs": {
                    "favorite_genre": "pop",
                    "favorite_mood": "happy",
                    "target_energy": 0.80,
                    "target_tempo_bpm": 120.0,
                    "target_valence": 0.90,
                    "target_danceability": 0.80,
                    "target_acousticness": 0.20
                },
                "expected_top_genre": "pop"
            }
        ]
        
        results = []
        for case in test_cases:
            logger.info(f"Running test case: {case['name']}")
            recs = agentic_recommend_workflow(case['prefs'], songs, k=3)
            top_genre = recs[0][0]['genre'] if recs else None
            avg_conf = sum(conf for _, _, _, conf in recs) / len(recs) if recs else 0
            critique = self_critique_recommendations(recs, case['prefs'])
            
            pass_fail = "PASS" if top_genre == case['expected_top_genre'] else "FAIL"
            results.append({
                "case": case['name'],
                "pass_fail": pass_fail,
                "avg_confidence": avg_conf,
                "top_genre": top_genre,
                "critique": critique
            })
        
        # Print summary
        print("\n=== Test Harness Summary ===")
        total_pass = sum(1 for r in results if r['pass_fail'] == "PASS")
        print(f"Overall: {total_pass}/{len(results)} tests passed")
        for r in results:
            print(f"- {r['case']}: {r['pass_fail']} (Confidence: {r['avg_confidence']:.2f}, Top Genre: {r['top_genre']})")
            print(f"  Critique: {r['critique']}")
        
        logger.info("Test harness completed")
        
    except Exception as e:
        logger.error(f"Error in test harness: {e}")
        raise


if __name__ == "__main__":
    run_test_harness()