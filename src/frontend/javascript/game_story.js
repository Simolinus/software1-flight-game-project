document.querySelector(".entername").style.visibility = "hidden";
document.getElementById("n-game").addEventListener("click", newGame);

async function newGame() {
  document.getElementById("n-game").style.display = "none";

  const response = await fetch("../../backend/game_story.txt");
  const text = await response.text();
  console.log(text);

  typeWriter(text, "story-area", 20);

}

function typeWriter(text, elementId, speed = 20) {
  const element = document.getElementById(elementId);
  element.textContent = "";

  let index = 0;

  function type() {
      console.log("text.length: ", text.length);
    if (index < text.length) {
        console.log("text: ", text.charAt(index));

      element.textContent += text.charAt(index);
      index++;
      setTimeout(type, speed);
    } else {
        document.querySelector(".entername").style.visibility = "visible";
    }
  }

  type();
}
