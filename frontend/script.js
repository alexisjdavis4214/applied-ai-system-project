const genreSelect = document.getElementById("genreSelect");
const moodSelect = document.getElementById("moodSelect");
const energySlider = document.getElementById("energySlider");
const valenceSlider = document.getElementById("valenceSlider");
const danceSlider = document.getElementById("danceSlider");
const acousticSlider = document.getElementById("acousticSlider");
const tempoSlider = document.getElementById("tempoSlider");
const energyValue = document.getElementById("energyValue");
const valenceValue = document.getElementById("valenceValue");
const danceValue = document.getElementById("danceValue");
const acousticValue = document.getElementById("acousticValue");
const tempoValue = document.getElementById("tempoValue");
const runButton = document.getElementById("runButton");
const processSteps = document.getElementById("processSteps");
const knowledgeText = document.getElementById("knowledgeText");
const recommendationsNode = document.getElementById("recommendations");
const critiqueText = document.getElementById("critiqueText");

const genres = [
  "ambient",
  "classical",
  "country",
  "electronic",
  "folk",
  "hip-hop",
  "indie pop",
  "jazz",
  "lofi",
  "pop",
  "reggae",
  "rock",
  "rnb",
  "synthwave"
];

const moods = [
  "chill",
  "confident",
  "calm",
  "dreamy",
  "happy",
  "heartfelt",
  "intense",
  "focused",
  "laid-back",
  "moody",
  "nostalgic",
  "relaxed"
];

const defaultSteps = [
  { id: "analyze", title: "Analyzing preferences", detail: "Checking genre, mood, and target audio features." },
  { id: "retrieve", title: "Retrieving context", detail: "Looking up genre and mood knowledge for better decisions." },
  { id: "score", title: "Scoring songs", detail: "Comparing every track against the user's taste profile." },
  { id: "rank", title: "Ranking selections", detail: "Sorting by relevance, score, and confidence." },
  { id: "critique", title: "Self-critique", detail: "Reviewing the recommendation set for reliability and fit." }
];

function populateSelectors() {
  genres.forEach((genre) => {
    const option = document.createElement("option");
    option.value = genre;
    option.textContent = genre;
    genreSelect.appendChild(option);
  });

  moods.forEach((mood) => {
    const option = document.createElement("option");
    option.value = mood;
    option.textContent = mood;
    moodSelect.appendChild(option);
  });

  genreSelect.value = "lofi";
  moodSelect.value = "chill";
}

function updateSliderLabels() {
  energyValue.textContent = energySlider.value;
  valenceValue.textContent = valenceSlider.value;
  danceValue.textContent = danceSlider.value;
  acousticValue.textContent = acousticSlider.value;
  tempoValue.textContent = tempoSlider.value;
}

function buildProcessStep(step, index) {
  const node = document.createElement("div");
  node.className = "process-step";
  if (index === 0) node.classList.add("active");
  node.innerHTML = `<h3>${step.title}</h3><p>${step.detail}</p>`;
  return node;
}

function showProcessSteps() {
  processSteps.innerHTML = "";
  defaultSteps.forEach((step) => {
    processSteps.appendChild(buildProcessStep(step));
  });
}

function animateSteps() {
  const stepNodes = Array.from(processSteps.children);
  stepNodes.forEach((node, idx) => {
    setTimeout(() => {
      node.classList.add("active");
    }, idx * 450);
  });
}

function renderRecommendations(recs) {
  recommendationsNode.innerHTML = "";
  if (!recs.length) {
    recommendationsNode.innerHTML = `<p class='empty-state'>Choose preferences and run the demo for personalized songs.</p>`;
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
  const userPrefs = {
    favorite_genre: genreSelect.value,
    favorite_mood: moodSelect.value,
    target_energy: parseFloat(energySlider.value),
    target_tempo_bpm: parseFloat(tempoSlider.value),
    target_valence: parseFloat(valenceSlider.value),
    target_danceability: parseFloat(danceSlider.value),
    target_acousticness: parseFloat(acousticSlider.value)
  };

  processSteps.innerHTML = "";
  showProcessSteps();
  animateSteps();

  knowledgeText.textContent = "Loading knowledge retrieval...";
  critiqueText.textContent = "Evaluating recommendations...";
  recommendationsNode.innerHTML = "";
  runButton.disabled = true;
  runButton.textContent = "Running...";

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(userPrefs)
    });
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }
    const data = await response.json();
    knowledgeText.textContent = data.knowledge;
    renderRecommendations(data.recommendations);
    critiqueText.textContent = data.critique;
  } catch (error) {
    knowledgeText.textContent = "Unable to retrieve knowledge.";
    critiqueText.textContent = "Recommendation service error.";
    recommendationsNode.innerHTML = `<p class='empty-state'>${error.message}</p>`;
  } finally {
    runButton.disabled = false;
    runButton.textContent = "Run Recommendation";
  }
}

function initialize() {
  populateSelectors();
  updateSliderLabels();
  showProcessSteps();
  renderRecommendations([]);
  [energySlider, valenceSlider, danceSlider, acousticSlider, tempoSlider].forEach((slider) => {
    slider.addEventListener("input", updateSliderLabels);
  });
  runButton.addEventListener("click", runRecommendationFlow);
}

initialize();
