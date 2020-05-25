import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import re
import urllib
import urllib.request
import jsonifySettings
import difflib
from pynput.keyboard import Key, Listener
from pynput.keyboard import Controller, KeyCode
import time
import scheduler
import threading

song_in_queue = None
ctrl_pressed = False
space_pressed = False
listen = False
apiKey = jsonifySettings.readSpecificSetting('settings.json', 'ytApiKey')
playRequests = False
r = sr.Recognizer()
r.energy_threshold = 1000
killYoutube = False
commands = ['play youtube', 'play requests', 'set botname']
botname ='baxter'
now_time = None
yt_video_seconds = None
song_id = None
path_to_extension = r'C:\Users\rpski\Desktop\4.10.0_0'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)
chrome_options.add_argument("chrome://flags/#enable-media-session-service")


# If launched from GUI, baxterRunning will == True
print(jsonifySettings.readSpecificSetting('settings.json', 'baxterRunning'))
if jsonifySettings.readSpecificSetting('settings.json', 'baxterRunning') == 1:
    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    except IndexError as e:
        pass
    driver.switch_to.window(driver.window_handles[0])


def click_play_button():
    keyboard = Controller()
    print('Pausing/Resuming... ')
    keyboard.press(KeyCode.from_vk(0xB3))  # Play/Pause

def set_volume(volume):
    driver.execute_script(f'''var videoElement = document.querySelector("video")
var audioCtx = new AudioContext()
var source = audioCtx.createMediaElementSource(videoElement)
var gainNode = audioCtx.createGain()
gainNode.gain.value = {volume}
source.connect(gainNode)
gainNode.connect(audioCtx.destination)''')

class youtube():
    global killYoutube, driver


    def __init__(self):
        print('Playing youtube video...')


    def playSong(self, search):
        global now_time, song_id
        global yt_video_seconds
        print(search)
        now_time = None
        if not search:
            return
        wait = WebDriverWait(driver, 20)
        time.sleep(1)
        presence = EC.presence_of_element_located
        visible = EC.visibility_of_element_located
        if 'youtube.com' in search[24:].lower():
            # Navigate to url with video being appended to search_query
            driver.get(search)
            # play the video
            wait.until(visible((By.ID, "video-title")))
            driver.find_element_by_id("video-title").click()
            print('Playing from link')
            yt_video_seconds = get_youtube_video_duration(search)
            # Auto close after getting duration of video
            duration = get_youtube_video_duration(driver.current_url)
            now_time = time.time()
            song_id = scheduler.new_task(time.time() + duration, next_song)


        else:
            # Navigate to url with video being appended to search_query
            driver.get("https://www.youtube.com/results?search_query=" + str(search.replace(" ", '+')))
            print(driver.current_url)
            # play the video
            wait.until(visible((By.ID, "video-title")))
            driver.find_element_by_id("video-title").click()
            print('Playing from video description')
            duration = get_youtube_video_duration(driver.current_url)
            print(duration)
            now_time = time.time()
            song_id = scheduler.new_task(time.time() + duration, next_song)
        return now_time



def print_requests():
    with open("songRequests.txt", "r") as f:
        print(f.readlines())


def eval_command_ratio(vd):
    # ratios always floats
    ratio = 0.75
    play_yt_ratio = 0.50
    commands = [f"{botname} play youtube", f"{botname} play requests", f"{botname} set bot name"]
    result = []
    for i in commands:
        match = difflib.SequenceMatcher(a=vd, b=i).ratio()
        result.append((i, match))
    vd = max(result, key=lambda x: x[1])
    # if the closest one is command[0]/botname play youtube, compare with play_yt_ratio
    if vd[0] == commands[0]:
        if vd[1] > play_yt_ratio:
            # todo remove print
            print(vd)
            return vd[0]
    if vd[1] > ratio:
        # todo remove print
        print(vd)
        return vd[0]


def strip_chats_brackets(text, repl):
    for c in "{}'":
        text = text.replace(c, repl)
    return text


def strip_chars_sec_duration(text, repl):
    for c in "PTS":
        text = text.replace(c, repl)
    return text


def look_for_request():
    nextUp = None
    with open('songRequests.txt', 'r+') as fin:
        data = fin.readlines()
        if data:
            nextUp = data[0]
    if nextUp:
        return nextUp


def delete_next_request():
    nextUp = None
    with open('songRequests.txt', 'r+') as fin:
        data = fin.readlines()
        if data:
            nextUp = data[0]
    with open('songRequests.txt', 'w') as fin:
        fin.write("".join(data[1:]))


def next_song():
    driver.get("https://www.youtube.com")
    delete_next_request()



def get_youtube_video_duration(videoLink):
    videoId = videoLink.split('=',1)[1]
    searchUrl=f'https://www.googleapis.com/youtube/v3/videos?id={videoId}&key={apiKey}&part=contentDetails'
    print(searchUrl)
    response = urllib.request.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data=data['items']
    contentDetails=all_data[0]['contentDetails']
    youtubes_duration_format=contentDetails['duration']
    return get_youtube_seconds_duration(youtubes_duration_format)


def get_youtube_seconds_duration(dur):
    seconds = 0
    matched = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", dur)
    print(matched)
    is_match = bool(matched)
    if matched:
        time = matched.group(1,2,3)
        for i in range(len(time)):
            if time[i]:
                seconds += int(time[i])*60**(2-i)
        print(seconds)
        return seconds


def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        try:
            voiceData = r.recognize_google(audio)
            if voiceData:
                jsonifySettings.writeSpecificSetting('settings.json', 'speaking', 0)
            print(voiceData)
            return voiceData
        except sr.UnknownValueError:
            print('Sorry I didnt get that')
            jsonifySettings.writeSpecificSetting('settings.json', 'speaking', 0)
        except sr.RequestError:
            jsonifySettings.writeSpecificSetting('settings.json', 'speaking', 0)
            print('Voice service is down')
 

def casePlayYoutube(vd):
    print('youtubeplay')
    print(vd)
    print(vd[19:].lower())
    if vd[19:].lower():
        toSearch = vd[19:].lower()
        print(toSearch)
        print('tst')
        uTube = youtube()
        uTube.playSong(toSearch)
    if not vd[19:]:
        print('Speak faster and better')


def casePlayRequests():
    print('case play requests')
    nextUp = look_for_request()
    if nextUp and len(nextUp) > 3:
        nextUp = strip_chats_brackets(nextUp, "").rstrip()
        song = nextUp.split(': ', 1)[1]
        user = nextUp.split(': ', 1)[0]
        uTube = youtube()
        return uTube.playSong(song)


def respond(voiceData):
    global botname
    if voiceData:
        diffed_command = eval_command_ratio(voiceData.lower())
        print(diffed_command)
        if diffed_command:
            if f"{botname} play youtube" == diffed_command[:19]:
                print('playing yt')
                casePlayYoutube(voiceData)
            elif f"{botname} play requests" == diffed_command:
                print('respond')
                casePlayRequests()
            elif "set name" == diffed_command:
                setBotName()
            else:
                print('Waiting for command')
                jsonifySettings.writeSpecificSetting('settings.json', 'speaking', 0)


def Main():
    global now_time, song_in_queue
    sched = threading.Thread(target=scheduler.scheduler, args=())
    sched.start()
    while True:
        time.sleep(.25)
        try:
            tmp = look_for_request()
            if jsonifySettings.readSpecificSetting('settings.json', 'autoPlaySR') and tmp != song_in_queue:
                song_in_queue = tmp
                casePlayRequests()
        except PermissionError as e:
            print(e)
        if space_pressed and ctrl_pressed:
            print('Pressed!')
            voiceData = record_audio()
            respond(voiceData)


def on_press(key):
    global ctrl_pressed, space_pressed
    if key == Key.ctrl_l and not ctrl_pressed:
        ctrl_pressed = True
    if key == Key.space and not space_pressed:
        space_pressed = True


def on_release(key):    # any key you want
    global song_id, ctrl_pressed, space_pressed
    if key == Key.scroll_lock:
        delete_next_request()
        scheduler.remove_task(song_id)
        song_id = None
        if driver:
            driver.get('https://www.youtube.com')
    if key == Key.page_up:
        scheduler.pause_task(song_id)
        if driver:
            click_play_button()
    if key == Key.ctrl_l and ctrl_pressed:
        ctrl_pressed = False
    if key == Key.space and space_pressed:
        space_pressed = False


with Listener(on_release=on_release, on_press=on_press) as listener:
    if jsonifySettings.readSpecificSetting('settings.json', 'baxterRunning') == 1:
        Main()
        listener.join()