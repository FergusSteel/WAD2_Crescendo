function playAudio() {
  var audio = document.getElementById("audiofile");
  var play = document.getElementById("topimage");
  console.log("image clicked")
  if (audio.paused) {
    audio.play();
    play.src = document.getElementById("var1").value;
  } else {
    audio.pause();
    play.src = document.getElementById("var2").value;
  }
}
