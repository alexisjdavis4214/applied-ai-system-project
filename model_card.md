# Model Card: Music Recommender AI System

**Model Name:** VibeFinder 1.0  
**Version:** 1.0  
**Author:** Alexis Davis  
**Date:** April 2026  
**Type:** Content-based recommendation system with RAG and agentic workflow

---

## 1. Intended Use

VibeFinder recommends songs from a curated 75-track catalog based on a user's stated preferences — their favorite genre, favorite mood, and five target audio features (energy, tempo, emotional positivity, danceability, and acousticness).

**Who it is for:** Anyone who wants personalized music recommendations without sharing their listening history. It is especially useful for people who already know what kind of music they are in the mood for and want the system to surface tracks that fit that profile precisely.

**What it assumes about the user:** The system assumes users can describe their preferences numerically or categorically. It does not learn from implicit signals like skips, replays, or listening time — it works entirely from what the user explicitly provides. It also assumes the user's taste can be represented as a single stable profile, which is not always true in practice.

**Classroom vs. real-world use:** This project was built as an applied AI learning exercise. The catalog, artists, and song titles are simulated. The architecture, scoring logic, confidence metrics, and self-evaluation patterns are all modeled on real production recommendation systems and are meant to demonstrate how those systems are designed and evaluated.

---

## 2. How the Model Works

Imagine you walk into a record store and describe exactly what you want: *"Something chill, lofi, not too fast, mostly acoustic, a little melancholy."* A knowledgeable clerk would mentally scan the shelves and pull out the tracks that best match each part of your description. VibeFinder does the same thing, automatically, for every song in the catalog.

Here is how it works step by step:

**Step 1 — You describe what you want.** You provide your favorite genre (like "lofi" or "jazz"), your favorite mood (like "chill" or "focused"), and five numbers between 0 and 1 representing how much energy, danceability, positivity, and acoustic texture you want, plus a target tempo in beats per minute.

**Step 2 — The system scores every song in the catalog.** For each of the 75 songs, it checks:
- Does the genre match yours? If yes: +2.0 points.
- Does the mood match yours? If yes: +1.0 points.
- How close is the song's energy to your target? The closer, the more points (up to +0.5).
- How close is the tempo? The closer, the more points (up to +0.4).
- The same check is done for emotional positivity (valence), danceability, and acousticness (up to +0.4 each).

The maximum a song can ever score is 5.1, which would only happen if it perfectly matched your genre, mood, and every numeric target simultaneously.

**Step 3 — The system ranks the top matches and assigns a confidence score.** Confidence is simply how much of that 5.1 maximum the top song actually achieved. A score of 5.05 / 5.1 = 99% confidence means the song is nearly perfect for your profile. A score of 2.1 / 5.1 = 41% confidence means the catalog had no great matches and the system is flagging that.

**Step 4 — The system critiques its own results.** Before showing you anything, VibeFinder checks its average confidence across the top 5 recommendations and whether the highest-ranked song actually matches your genre and mood. If confidence is low or the top song doesn't match, the system says so — it will not pretend a mediocre recommendation is a good one.

**What changed from the starter version:** The original project computed confidence as how far ahead the top song was from its nearest competitor. This meant that when many songs scored similarly — which happens often in a large, diverse catalog — confidence would collapse to near zero even for recommendations that were objectively excellent. The formula was changed to measure confidence against the theoretical maximum instead, which made the metric honest and useful.

---

## 3. Data

**Catalog size:** 75 songs, each described by 10 attributes: a unique ID, title, artist name, genre, mood, energy (0–1), tempo in BPM, valence (emotional positivity, 0–1), danceability (0–1), and acousticness (0–1).

**Genres represented (19 total):** lofi, pop, rock, ambient, jazz, synthwave, indie pop, classical, hip-hop, country, electronic, folk, reggae, R&B, metal, blues, Latin, trap, and soul.

**Moods represented (16 total):** chill, happy, intense, moody, focused, relaxed, nostalgic, confident, heartfelt, dreamy, calm, laid-back, romantic, uplifting, energetic, and dark.

**Energy and tempo spread:** Songs range from very low energy (0.16) to near maximum (0.98), and from 54 BPM to 180 BPM, covering slow ambient pieces through extreme metal and Latin dance.

**How the data was built:** The catalog started with 17 hand-crafted songs and was expanded to 75 by generating new entries with intentional variety across genres, moods, energy bands, and tempo ranges. Each song's numeric values were chosen to reflect the real-world characteristics of its genre — for example, ambient songs cluster around 0.15–0.30 energy and 54–64 BPM, while metal songs cluster near 0.94–0.98 energy and 160–176 BPM.

**What is missing:** The catalog does not represent global music traditions beyond Western and Caribbean genres. K-pop, Afrobeats, qawwali, bossa nova, and many other widely listened-to styles are absent. All artists are simulated — there are no real-world artists, albums, or track lengths, which means the data cannot capture important real signals like an artist's established fanbase or a song's cultural moment. The system also has no data on lyrics, meaning it cannot distinguish between a happy-sounding song with sad lyrics and a genuinely uplifting one.

---

## 4. Strengths

**Clear preference profiles.** VibeFinder performs best when a user's preferences are specific and internally consistent. A user who knows they want low-energy, acoustic, chill lofi at around 78 BPM will receive recommendations with confidence scores above 0.95 because the catalog has multiple songs purpose-built for that profile.

**Transparency.** Every recommendation comes with a line-by-line breakdown of what contributed to its score. A user can look at the output and see exactly which features drove the match and which ones missed. This is a meaningful advantage over black-box systems that give you a recommendation with no explanation.

**Self-awareness.** The self-critique layer catches cases where the system is not performing well. If no song in the catalog closely matches the user's preferences, the average confidence score will reflect that, and the critique will say so explicitly rather than presenting a weak recommendation as if it were strong.

**Consistency.** Given the same preferences, the system always produces the same ranked list in the same order. There is no randomness. This makes the system easy to test, debug, and reason about.

**Genre and mood prioritization.** Putting the heaviest weight on genre and mood (+2.0 and +1.0) means that a jazz fan will never have a metal song appear at the top of their list, no matter how well the numeric features align. This matches the intuition that categorical fit is the most important signal for music taste.

---

## 5. Limitations and Bias

**No learning.** The system never updates based on what a user actually liked or skipped. Every session starts from scratch. A user who repeatedly ignores lofi recommendations and plays jazz will receive the same recommendations the next time they log in.

**Catalog limits discovery.** The system can only recommend songs it already knows about. A user whose real taste sits between two genres — say, experimental jazz-electronic fusion — will receive the closest available match, not a genuinely fitting one.

**Genre and mood weights may over-constrain.** Because genre is worth twice as much as all the numeric features combined, a song that is a perfect numeric match but the wrong genre will always rank below a genre-matching song with mediocre numeric similarity. This is appropriate most of the time but can frustrate users with eclectic tastes who care more about energy or tempo than genre labels.

**Western genre dominance.** The 19 genres in the catalog skew heavily toward Western pop, rock, and electronic traditions. Users whose primary listening includes genres not represented — Afrobeats, cumbia, Bollywood, classical Indian, etc. — will receive poor recommendations because the catalog cannot match their actual taste.

**Simulated data.** The numeric values for each song were carefully chosen to reflect genre norms but were not derived from audio analysis of real tracks. A real system would extract features directly from audio waveforms using tools like librosa or the Spotify audio features API, producing values that reflect actual acoustic content rather than reasonable estimates.

**No lyrical, cultural, or social awareness.** Two songs with identical genre, mood, and numeric profiles but very different lyrical content — one celebratory, one about grief — will score identically. The system has no way to distinguish them.

**Single-profile assumption.** The system models each user as one stable preference vector. Real music listeners switch contexts constantly — studying, working out, falling asleep, celebrating — and a single profile cannot represent that range.

---

## 6. Evaluation

**Test suite:** 7 automated unit tests cover core functions. 6 of 7 pass. The one failure — `test_explain_recommendation_returns_non_empty_string` — exposes a real gap: the object-oriented `Recommender.explain_recommendation()` method returns a placeholder string and has not been connected to the actual scoring logic yet.

**Test harness:** A separate evaluation script runs two predefined user profiles (a lofi/chill listener and a pop/happy listener) and checks whether the top recommendation matches the expected genre. Both pass.

**Confidence scores before and after the formula fix:** Before the fix, average confidence hovered around 0.15–0.27 even for near-perfect matches, and the self-critique always reported "low confidence." After redefining confidence as `score / 5.1`, a lofi/chill profile now yields average confidence of ~0.95 for the top recommendations, which accurately reflects how well the catalog matches that profile.

**What was tested manually:**
- Lofi/chill profile → top 3 results were all lofi/chill songs with scores above 5.0
- Pop/happy profile → top 2 results were both pop/happy songs
- A deliberately mismatched profile (e.g., pop genre preference with low energy and high acousticness targets) → top song matched genre but showed lower confidence (~0.80), and the critique noted partial alignment — correct behavior
- An empty preferences dict → recommendation still ran but returned results with no genre or mood bonus; confidence reflected that

**What surprised me:** The self-critique reporting "low confidence" while simultaneously saying "top recommendation strongly matches user preferences" was a clear contradiction that went unnoticed for several iterations. It took actively reading the output with skepticism — rather than just checking that it ran — to catch it. That was a lesson in evaluation: a system that produces output without crashing is not the same as a system that is working correctly.

---

## 7. Future Work

**Learn from feedback.** The highest-value improvement would be collecting implicit signals — songs played through vs. skipped, replayed tracks, session-end ratings — and using them to update user preference vectors over time. Even a simple weighted moving average of confirmed preferences would produce meaningfully better results than a static profile.

**Complete the `explain_recommendation` method.** The OOP `Recommender` class has a stub that returns a placeholder. Connecting it to the scoring logic from `score_song()` would make the object-oriented API fully functional and consistent with the functional API.

**Add diversity enforcement.** The current system can return five songs by the same artist if they all score highest. A post-processing step that penalizes repeated artists or genres in the top-k results would improve the perceived variety and usefulness of recommendations.

**Expand the catalog with real audio features.** Replacing the manually estimated numeric values with features extracted from actual audio (using librosa, essentia, or an audio features API) would make the scoring reflect genuine acoustic content rather than genre conventions.

**Add more underrepresented genres.** At minimum, Afrobeats, bossa nova, K-pop, and classical Indian traditions should be represented. Each addition makes the system meaningful for a wider range of users.

**Support multi-context profiles.** Allow users to save multiple preference profiles — "study mode," "gym mode," "evening wind-down" — and switch between them. This would better reflect how people actually use music throughout their day.

**Implement playlist-length recommendations.** Currently the system returns k individual songs. Recommending a coherent 30- or 60-minute playlist with controlled variety (energy arc, genre transitions) would be a more useful real-world output.

---

## 8. Personal Reflection

Building this system changed how I think about recommendation algorithms in everyday apps. Before this project, I thought of Spotify's Discover Weekly as something that just works — a magic black box that somehow knows what I want. Now I see it as a pipeline with the same structural pieces as VibeFinder: a feature representation of content, a model of user preference, a scoring function that compares the two, and an evaluation layer that catches failures before they reach the user. The specific algorithms Spotify uses are far more complex, but the questions they are answering are the same ones I had to answer here.

The most unexpected discovery was how much of evaluation is about *reading your own output with suspicion*. I had a self-critique module that was generating text that looked like it was working, but the numbers it was reporting were wrong in a way that was only obvious if you stopped and thought about whether the output made sense. The fix was not complicated once I understood it — but finding it required a kind of active skepticism that I had to learn to apply deliberately. I think that is a skill that matters in any context where an AI system produces outputs that look plausible even when they are not.
