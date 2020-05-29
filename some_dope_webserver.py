import hug

song_queue = []


def look_for_current_request():
    if song_queue[0] is not None:
        user = ["user"]
        song = song_queue[0].values()
        print(user, song)
        return user, song
    else:
        return None

# def look_for_current_request():
#     next_up = None
#     with open('songRequests.txt', 'r+') as fin:
#         data = fin.readlines()
#         if data:
#             next_up = data[0]
#     if next_up is not "\n" and next_up is not None:
#         user = next_up[:next_up.index(":")].replace("{", "")
#         song = next_up[next_up.index(":"):].replace("}", "")
#         song = song.replace(":  ", "")
#         song = song.rstrip("\n")
#         return user, song
#     else:
#         user = ""
#         song = "No song in que!"
#         return user, song

def look_for_next_request():
    if song_queue[1] is not None:
        user = song_queue[0].keys()
        song = song_queue[0].values()
        return user, song
    else:
        return None

# def look_for_next_request():
#     next_up = None
#     with open('songRequests.txt', 'r+') as fin:
#         data = fin.readlines()
#         if data:
#             next_up = data[1]
#     print(next_up)
#     if next_up is not "\n" and next_up is not None:
#         user = next_up[:next_up.index(":")].replace("{", "")
#         song = next_up[next_up.index(":"):].replace("}", "")
#         song = song.replace(":  ", "")
#         song = song.rstrip("\n")
#         return user, song
#     else:
#         user = ""
#         song = "No song in que!"
#         return user, song


@hug.get("/music")
@hug.local()
def music():
    """Returns current song playing and user who requested it"""
    user, song = look_for_current_request()
    next_user, next_song = look_for_next_request()
    return {'user': user, 'song': song, 'next_user': next_user, 'next_song': next_song}

# @hug.post("/random_user_quote", output=hug.output_format.json)
# def add_song():
#     song_queue.append({user: song})

@hug.post("/add_song", output=hug.output_format.json)
def add_song(user, song):
    song_queue.append({user: song})


@hug.get("/client", output=hug.output_format.file)
def client():
    return "./Client/client.html"


@hug.get("/client_styles.css", output=hug.output_format.file)
def client_styles():
    return "./Client/styles.css"


@hug.get("/client_scripts.js", output=hug.output_format.file)
def client_scripts():
    return "./Client/scripts.js"


@hug.get("/favicon.ico")
def favicon():
    raise falcon.HTTPForbidden("fuck you")


@hug.get("/music_thing", output=hug.output_format.file)
def music_thing():
    return "./nowPlaying.html"


@hug.get("/styles.css", output=hug.output_format.file)
def music_thing_css():
    return "./styles.css"


@hug.get("/scripts.js", output=hug.output_format.file)
def music_thing_js():
    return "./scripts.js"


# if __name__=="__main__":
