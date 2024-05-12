let cursor = document.getElementById("myCursor");
let circle = document.getElementById("circle");

function updateCursorPosition(e) {
  let x = e.pageX;
  let y = e.pageY;
  cursor.style.left = x - 5 + "px";
  cursor.style.top = y - 5 + "px";
  circle.style.left = x - 19 + "px";
  circle.style.top = y - 19 + "px";
}

window.addEventListener("mousemove", updateCursorPosition);
window.addEventListener("scroll", updateCursorPosition);