let user_el = undefined,
    song_el = undefined,
    next_user = undefined,
    next_song = undefined;

function updateDOM(data) {
    user_el.innerText = data.user;
    song_el.innerText = data.song;
    next_user.innerText = data.next_user;
    next_song.innerText = data.next_song;

}

function current_song() {
    let URL = 'http://localhost:8000/music';
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", URL, false);
    xmlHttp.send(null);
    console.log(xmlHttp.responseText);
    updateDOM(JSON.parse(xmlHttp.responseText));
}

document.addEventListener("DOMContentLoaded", function() {
    user_el = document.getElementById("user");
    song_el = document.getElementById("song");
    next_song = document.getElementById("nextUserSong");
    next_user = document.getElementById("nextUser");
    setInterval(current_song, 2500);
});