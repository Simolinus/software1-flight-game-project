document.addEventListener("DOMContentLoaded", async () => {
  const resPlayer = await fetch("http://127.0.0.1:3000/player");
  const player = await resPlayer.json();
  document.querySelector("#score").textContent = player.score;
});
