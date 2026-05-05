document.querySelector(".entername").style.visibility = "hidden";
document.getElementById("n-game").addEventListener("click", newGame);

async function newGame() {
  document.getElementById("n-game").style.display = "none";
  const response = await fetch("../../backend/game_story.txt");
  const text = await response.text();
  typeWriter(text, "story-area", 20);
}

function typeWriter(text, elementId, speed = 20) {
  const element = document.getElementById(elementId);
  element.textContent = " ";
  element.style.opacity = "1";
  let index = 0;
  function type() {
    if (index < text.length) {
      element.textContent += text.charAt(index);
      index++;
      setTimeout(type, speed);
    } else {
        document.querySelector(".entername").style.visibility = "visible";
    }
  }
  type();
}
