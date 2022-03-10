function playAudio() {
  var audio = document.getElementById("audiofile");
  console.log("image clicked")
  if (audio.paused) {
    audio.play();
  } else {
    audio.pause();
  }
}
