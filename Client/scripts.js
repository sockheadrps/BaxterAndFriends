
var socket = new WebSocket("ws://localhost:8765/");
socket.onopen = function (event) {
    socket.send("CONNECT")
};
socket.onmessage = function (event) {
    console.log(event.data);
}


function updateSlider(val) {
    console.log(val.childNodes)
    let span = val.childNodes[2]
    let input = val.childNodes[1]
    input.oninput = function() {
        span.innerText=input.value;
    };
    input.oninput();
    input.onmouseup = function() {
        let {id, value} = input;
        console.log(id)
        socket.send(JSON.stringify({[id]: parseInt(value)}));

    };

}
// Update the current slider value (each time you drag the slider handle)
document.addEventListener("DOMContentLoaded", function() {
    let sounds_slider = document.getElementById("sounds-cooldown");
    let tts_slider = document.getElementById("tts-max-chars");
    console.log(sounds_slider, tts_slider)
    updateSlider(sounds_slider);
    updateSlider(tts_slider);
});

