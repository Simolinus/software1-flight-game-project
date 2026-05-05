export const BASE_URL = "http://127.0.0.1:3000";

export async function startNewGame(screen_name) {
  const res = await fetch(`${BASE_URL}/start-new-game`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ screen_name }),
  });
  return await res.json();
}

export async function getAirports() {
  const res = await fetch(`${BASE_URL}/airports`);
  return await res.json();
}

export async function getPlayer() {
  const res = await fetch(`${BASE_URL}/player`);
  return await res.json();
}

export async function updatePlayer(money, score) {
  const res = await fetch(`${BASE_URL}/player-update`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      screen_name: window.screen_name,
      money: window.money,
      score: window.score,
    }),
  });

  const data = await res.json();
  console.log("update result:", data);
}

export async function getPlayerLocation() {
  const res = await fetch(`${BASE_URL}/playerlocation`);
  return await res.json();
}

export async function getMapData() {
  const res = await fetch(`${BASE_URL}/map-data`);
  return await res.json();
}

export async function travel(destination, type) {
  const res = await fetch(`${BASE_URL}/travel`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ destination, type }),
  });
  return await res.json();
}

export async function getClue() {
  const res = await fetch(`${BASE_URL}/clue`);
  const data = await res.json();
  console.log("data.clue: ", data);
  document.querySelector(".clue_class").textContent = data;
}
window.addEventListener("load", getClue);
document.addEventListener("DOMContentLoaded", getClue);

export async function countAcquiredPuzzles() {
  const res = await fetch(`${BASE_URL}/count-acquired-puzzles`);
  const data = await res.json();
  return data.count;
}

window.screen_name = null;
window.money = null;
window.score = null;
window.refreshPlayerUI = refreshPlayerUI;
document.addEventListener("DOMContentLoaded", refreshPlayerUI);
window.addEventListener("playerUpdated", refreshPlayerUI);
export async function refreshPlayerUI() {
  console.log("window:  ", window.screen_name, window.money, window.score);
  const p = await getPlayer();
  const count = await countAcquiredPuzzles();

  console.log("refreshPlayerUI: ", p.screen_name, p.money, p.score);
  if (window.screen_name != null) {
    document.querySelector("#name").textContent = window.screen_name;
  } else {
    document.querySelector("#name").textContent = p.screen_name;
    window.screen_name = p.screen_name;
  }
  if (window.money != null) {
    document.querySelector("#coin").textContent = window.money;
  } else {
    document.querySelector("#coin").textContent = p.money;
    window.money = p.money;
  }
  document.querySelector("#puzzle").textContent = count;
  document.querySelector("#location").textContent = p.location;
}

window.getQuiz = getQuiz;
document.addEventListener("DOMContentLoaded", getQuiz);
export async function getQuiz() {
  const res = await fetch(`${BASE_URL}/quiz`);
  const data = await res.json();
  const quiz = data[0][1];
  window.answer = data[0][2];
  console.log("js-getquiz:", quiz);
  console.log("js-answer:", window.answer);
  document.querySelector(".qui").textContent = data[0][1];
}

window.answer = "";
document.addEventListener("DOMContentLoaded", () => {
  const submitBtn = document.querySelector("#submit");
  const answerInput = document.querySelector("#answer");

  submitBtn.addEventListener("click", () => {
    const answer = answerInput.value.trim().toUpperCase();
    if (answer == window.answer) {
      alert("Congratulation!  Money: +100!  Score: +1");
      window.money += 100;
      window.score += 1;
      updatePlayer(window.money, window.score);
      const event = new Event("playerUpdated");
      window.dispatchEvent(event);
    } else {
      alert("Wrong answer! Try again!");
    }
  });
});
