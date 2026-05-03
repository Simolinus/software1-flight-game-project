import { getClue } from "./api.js";

async function loadClue() {
    const data = await getClue();
    console.log("data.clue: ", data);
    document.querySelector(".clue_class").textContent = data;
}

window.addEventListener("load", loadClue);

