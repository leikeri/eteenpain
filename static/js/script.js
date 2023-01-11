

    var x = document.getElementById("playAudio");
    function playAudio() {
        x.play();
        x.pauseOnBlur = false;
    }

    function pauseAudio() {
        x.pause();
    }
