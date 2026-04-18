# Music Recommender with AI Enhancements

## Original Project Summary
This project originated as the **Music Recommender Simulation** from Modules 1-3, where the goal was to build a small music recommender system. It represented songs and user "taste profiles" as data, designed a scoring algorithm to match songs to preferences, evaluated the system's right and wrong predictions, and reflected on how this mirrors real-world AI recommenders like Spotify. The original capabilities included loading song data, scoring based on genre/mood matches and numeric similarities, and outputting ranked recommendations with explanations.

## Project Summary
This enhanced music recommender system uses AI to suggest songs based on user preferences, incorporating reliability features, retrieval-augmented generation (RAG), agentic multi-step workflows, and automated testing. It matters because it demonstrates practical AI application in recommendation systems, emphasizing reliability, transparency, and self-evaluation—key for building trustworthy AI in real-world scenarios like content personalization.

## Architecture Overview
The system follows a modular architecture with observable data flow:
- **Components**: Data Loader (loads songs), Knowledge Retriever (RAG from JSON), Scorer (computes similarities), Agentic Workflow Orchestrator (manages steps), Self-Critique (evaluates outputs), and Test Harness (automated evaluation).
- **Data Flow**: User preferences → Load data → Analyze/Retrieve → Score/Rank with confidence → Self-critique → Output recommendations.
- **Human/Testing Involvement**: Humans input preferences and review outputs for refinement; automated tests check consistency, validation, and performance, with self-critique providing AI feedback.

```mermaid
graph TD
    A[User Input: Preferences] --> B[Data Loader: Load Songs from CSV]
    B --> C[Agentic Workflow Orchestrator]
    C --> D[Knowledge Retriever: Fetch from knowledge.json (RAG)]
    C --> E[Scorer: Calculate song scores based on prefs]
    D --> F[Ranker: Sort songs, add confidence scores]
    E --> F
    F --> G[Self-Critique: Evaluate recommendations]
    G --> H[Output: Recommendations with scores, confidence, reasons, critique]
    H --> I[Human Review: Check results, refine preferences if needed]

    J[Test Harness: Run predefined test cases] --> K[Evaluator: Check pass/fail, consistency, confidence]
    K --> L[Test Summary: Pass/fail scores, critiques]
    L --> I

    style A fill:#e1f5fe
    style H fill:#c8e6c9
    style I fill:#fff3e0
    style L fill:#fce4ec
```

## Setup Instructions
1. Ensure Python 3.8+ is installed.
2. Clone or navigate to the project directory.
3. Install dependencies: `pip install -r requirements.txt`
4. Run the main recommender: `python src/main.py`
5. Run the test harness: `python src/test_harness.py`
6. Run unit tests: `python -m pytest tests/ -v`

## Sample Interactions
Here are examples of inputs and outputs, demonstrating functionality:

### Example 1: Lofi Chill Preferences
**Input**: `{"favorite_genre": "lofi", "favorite_mood": "chill", "target_energy": 0.4, "target_tempo_bpm": 78.0, "target_valence": 0.58, "target_danceability": 0.6, "target_acousticness": 0.78}`

**Output**:
```
Top Recommendations:
1. Midnight Coding
   Score: 5.05
   Confidence: 0.01
   Reasons: genre match (+2.0), mood match (+1.0), energy similarity (0.98) × 0.5 = +0.49, ...

Self-Critique: Average confidence: 0.16. Low confidence; consider refining preferences. Top recommendation strongly matches user preferences.
```

### Example 2: Pop Happy Preferences
**Input**: `{"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "target_tempo_bpm": 120.0, "target_valence": 0.9, "target_danceability": 0.8, "target_acousticness": 0.2}`

**Output**:
```
Top Recommendations:
1. Sunrise City
   Score: 4.8
   Confidence: 0.05
   Reasons: genre match (+2.0), mood match (+1.0), valence similarity (0.96) × 0.4 = +0.38, ...

Self-Critique: Average confidence: 0.27. Low confidence; consider refining preferences. Top recommendation strongly matches user preferences.
```

### Example 3: Test Harness Summary
**Input**: Predefined test cases (e.g., Lofi Chill, Pop Happy).

**Output**:
```
=== Test Harness Summary ===
Overall: 2/2 tests passed
- Lofi Chill User: PASS (Confidence: 0.17, Top Genre: lofi)
  Critique: Average confidence: 0.17. Low confidence; consider refining preferences...
- Pop Happy User: PASS (Confidence: 0.27, Top Genre: pop)
  Critique: Average confidence: 0.27. Low confidence; consider refining preferences...
```

## Decisions and Trade-Offs
- **AI Enhancements**: Implemented RAG for contextual knowledge and agentic workflow for multi-step reasoning, but removed OpenAI fine-tuning due to API quota issues. Fell back to rule-based explanations for reliability.
- **Reliability**: Added logging, error handling, and guardrails (e.g., input validation) to ensure robustness without external dependencies.
- **Testing**: Comprehensive unit tests and a test harness for validation, focusing on consistency and edge cases.
- **Data**: Used CSV for songs and JSON for knowledge to keep it simple and offline.
- **Architecture**: Modular design with separate files for core logic, tests, and harness to facilitate maintenance.
- **Trade-Offs**: No external APIs for portability; rule-based scoring over ML for simplicity and explainability.

## Testing
- **Unit Tests**: `pytest tests/test_recommender.py` - Tests core functions, error handling, and validation.
- **Test Harness**: `python src/test_harness.py` - Evaluates predefined scenarios for consistency.
- **Results**: All tests pass (7/7 unit tests, 2/2 harness tests). Ensures reliability and correctness.

## Reflection
This project demonstrates building a robust AI system from scratch, incorporating advanced features like RAG and agentic workflows. Key learnings include handling API failures gracefully, the importance of testing, and creating clear documentation. It showcases skills in Python, AI concepts, and software engineering best practices, making it ideal for portfolio presentation.

## Model Card
See [model_card.md](model_card.md) for detailed model information, including intended use, limitations, and ethical considerations.

