export const BASE_URL = "http://127.0.0.1:3000";

export async function startNewGame(screen_name) {
    const res = await fetch(`${BASE_URL}/start-new-game`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ screen_name })
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
        body: JSON.stringify({ destination, type })
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


export async function refreshPlayerUI() {
  const p = await getPlayer();
  const count = await countAcquiredPuzzles();

  document.querySelector("#name").textContent = p.screen_name;
  document.querySelector("#coin").textContent = p.money;
  document.querySelector("#puzzle").textContent = count;
  document.querySelector("#location").textContent = p.location;
}
window.refreshPlayerUI = refreshPlayerUI;
document.addEventListener("DOMContentLoaded", refreshPlayerUI);

export async function getQuiz() {
    const res = await fetch(`${BASE_URL}/quiz`);
    const data = await res.json();
    const quiz = data[0][1];
    window.answer = data[0][2];
    console.log("js-getquiz:", quiz);
    console.log("js-answer:", window.answer);

    //document.querySelector("#qui").textContent = data[0][1];
    document.querySelector(".qui").textContent = data[0][1];

    //return data;
}
window.getQuiz = getQuiz;
document.addEventListener("DOMContentLoaded", getQuiz);

window.answer = "";
document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.querySelector("#submit");
    const answerInput = document.querySelector("#answer");

    submitBtn.addEventListener("click", () => {
        const answer = answerInput.value.trim();
        if(answer == window.answer) {
            alert("Congratulation!  Money: +100!  Score: +1");
        } else {
            alert("Wrong answer! Try again!");
        }
    });
});

