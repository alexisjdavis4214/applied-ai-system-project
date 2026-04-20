const vibeInput        = document.getElementById("vibeInput");
const runButton        = document.getElementById("runButton");
const processSteps     = document.getElementById("processSteps");
const knowledgeText    = document.getElementById("knowledgeText");
const recommendationsNode = document.getElementById("recommendations");
const critiqueText     = document.getElementById("critiqueText");
const interpretedPrefs = document.getElementById("interpretedPrefs");
const prefChips        = document.getElementById("prefChips");
const featureBars      = document.getElementById("featureBars");

const defaultSteps = [
  { title: "Parsing vibe",       detail: "Reading your words to detect genre, mood, and audio feature signals." },
  { title: "Retrieving context", detail: "Looking up genre and mood knowledge for better decisions." },
  { title: "Scoring songs",      detail: "Comparing every track against the translated taste profile." },
  { title: "Ranking selections", detail: "Sorting by relevance, score, and confidence." },
  { title: "Self-critique",      detail: "Reviewing the recommendation set for reliability and fit." }
];

function showProcessSteps() {
  processSteps.innerHTML = "";
  defaultSteps.forEach((step) => {
    const node = document.createElement("div");
    node.className = "process-step";
    node.innerHTML = `<h3>${step.title}</h3><p>${step.detail}</p>`;
    processSteps.appendChild(node);
  });
}

function animateSteps() {
  Array.from(processSteps.children).forEach((node, idx) => {
    setTimeout(() => node.classList.add("active"), idx * 450);
  });
}

function featureBar(label, value, displayLabel) {
  const pct = Math.round(value * 100);
  const display = displayLabel || `${pct}%`;
  return `
    <div class="feature-bar-row">
      <span class="feature-bar-label">${label}</span>
      <div class="feature-bar-track">
        <div class="feature-bar-fill" style="width:${pct}%"></div>
      </div>
      <span class="feature-bar-value">${display}</span>
    </div>`;
}

function displayInterpretedPrefs(prefs) {
  prefChips.innerHTML = `
    <div class="pref-chip genre-chip">Genre <strong>${prefs.favorite_genre}</strong></div>
    <div class="pref-chip mood-chip">Mood <strong>${prefs.favorite_mood}</strong></div>
  `;
  const tempoPct = (prefs.target_tempo_bpm - 40) / (180 - 40);
  featureBars.innerHTML =
    featureBar("Energy",       prefs.target_energy) +
    featureBar("Valence",      prefs.target_valence) +
    featureBar("Danceability", prefs.target_danceability) +
    featureBar("Acousticness", prefs.target_acousticness) +
    featureBar("Tempo",        tempoPct, `${Math.round(prefs.target_tempo_bpm)} BPM`);
  interpretedPrefs.classList.add("visible");
}

function renderRecommendations(recs) {
  recommendationsNode.innerHTML = "";
  if (!recs.length) {
    recommendationsNode.innerHTML = `<p class="empty-state">Describe your vibe and run AuraTune for personalized songs.</p>`;
    return;
  }
  recs.forEach((rec, index) => {
    const card = document.createElement("div");
    card.className = "track-card";
    card.innerHTML = `
      <div class="track-art">${index + 1}</div>
      <div class="track-meta">
        <h3>${rec.song.title}</h3>
        <div class="artist">${rec.song.artist}</div>
        <div class="track-tags">
          <span class="track-tag">${rec.song.genre}</span>
          <span class="track-tag">${rec.song.mood}</span>
        </div>
        <div class="track-score">
          <span><strong>Score</strong>: ${rec.score.toFixed(2)}</span>
          <span class="confidence-chip">Confidence ${rec.confidence.toFixed(2)}</span>
          <span>${rec.reasons.slice(0, 3).join(" • ")}</span>
        </div>
      </div>
    `;
    recommendationsNode.appendChild(card);
  });
}

async function runRecommendationFlow() {
  const vibeText = vibeInput.value.trim();
  if (!vibeText) {
    vibeInput.focus();
    vibeInput.classList.add("shake");
    setTimeout(() => vibeInput.classList.remove("shake"), 500);
    return;
  }

  showProcessSteps();
  animateSteps();
  knowledgeText.textContent = "Loading knowledge retrieval...";
  critiqueText.textContent = "Evaluating recommendations...";
  recommendationsNode.innerHTML = "";
  interpretedPrefs.classList.remove("visible");
  runButton.disabled = true;
  runButton.textContent = "Reading your vibe...";

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ vibe_text: vibeText })
    });
    if (!response.ok) throw new Error(`Request failed: ${response.status}`);
    const data = await response.json();

    if (data.parsed_prefs) displayInterpretedPrefs(data.parsed_prefs);
    knowledgeText.textContent = data.knowledge;
    renderRecommendations(data.recommendations);
    critiqueText.textContent = data.critique;
  } catch (error) {
    knowledgeText.textContent = "Unable to retrieve knowledge.";
    critiqueText.textContent = "Recommendation service error.";
    recommendationsNode.innerHTML = `<p class="empty-state">${error.message}</p>`;
  } finally {
    runButton.disabled = false;
    runButton.textContent = "Translate My Vibe";
  }
}

function initialize() {
  showProcessSteps();
  renderRecommendations([]);

  document.querySelectorAll(".example-chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      vibeInput.value = chip.dataset.vibe;
      vibeInput.focus();
    });
  });

  runButton.addEventListener("click", runRecommendationFlow);
}

initialize();
