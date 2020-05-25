import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
import re
import urllib
import urllib.request
from time import sleep
import songRequests
import jsonifySettings
import difflib
from pynput.keyboard import Key, Listener
from pynput.keyboard import Controller, KeyCode
import time
import timer


apiKey = jsonifySettings.readSpecificSetting('settings.json', 'ytApiKey')
playRequests = False
r = sr.Recognizer()
killYoutube = False
commands = ['play youtube', 'play requests', 'set botname']
botname ='baxter'
now_time = None
yt_video_seconds = None

path_to_extension = r'C:\Users\rpski\Desktop\4.10.0_0'
chrome_options = Options()
chrome_options.add_argument('load-extension=' + path_to_extension)
chrome_options.add_argument("chrome://flags/#enable-media-session-service")
# chrome_options.add_argument("--headless")
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

class youtube():
    global killYoutube, driver

    def __init__(self):
        print('Playing youtube video...')


    def playSong(self, search):
        global now_time
        global yt_video_seconds
        now_time = None
        try:
            wait = WebDriverWait(driver, 3)
            presence = EC.presence_of_element_located
            visible = EC.visibility_of_element_located
            if 'youtube.com' in search:
                # Navigate to url with video being appended to search_query
                driver.get(search)
                openPage = driver.current_url
                # play the video
                wait.until(visible((By.ID, "video-title")))
                driver.find_element_by_id("video-title").click()
                print('Playing from link')
                yt_video_seconds = get_youtube_video_duration(search)
                play_button = driver.find_element_by_xpath(
                    "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[1]/div/div/div/ytd-player/div/div/div[26]/div[2]/div[1]/button")
                play_button.click()
                # Auto close after getting duration of video
                now_time = time.time()
                timer.new_task(time.time() + yt_video_seconds, driver.close)
            else:
                # Navigate to url with video being appended to search_query
                driver.get("https://www.youtube.com/results?search_query=" + str(search.replace(" ", '+')))
                print(driver.current_url)

                # play the video
                wait.until(visible((By.ID, "video-title")))
                driver.find_element_by_id("video-title").click()
                print('Playing from video description')
                duration = int(get_youtube_video_duration(driver.current_url)) + 10
                now_time = time.time()
                timer.new_task(time.time() + yt_video_seconds, driver.close)
            return now_time
        except Exception as e:
            print(e)

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
    with open('songRequests.txt', 'r+') as fin:
        data = fin.readlines()
        if data:
            nextUp = data[0]
    with open('songRequests.txt', 'w') as fin:
        fin.write("".join(data[1:]))
    print(data)
    print(nextUp)
    print(("".join(data[1:])))
    if nextUp:
        return nextUp
    else:
        print('No song requests')


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
    matched = re.match(r"\w*?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)", dur)
    is_match = bool(matched)
    time = matched.group(1,2,3)
    for i in range(len(time)):
        if time[i]:
            seconds += int(time[i])*60**(2-i)
    print(seconds)
    return seconds


def setBotName():
    botNames = []
    for x in range(3):
        print(x)
        if x == 0:
            print('Speak your bot name')
            botNames.append(record_audio())
            continue
        if x == 1:
            print('Okay, again for reference')
            botNames.append(record_audio())
            continue
        if x == 2:
            print('One more time please')
            botNames.append(record_audio())

        

        # botNames = list(set(botNames))
        return botNames




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


def casePlayRequests(vd):
    nextUp = look_for_request()
    nextUp = strip_chats_brackets(nextUp, "").rstrip()
    song = nextUp.split(': ', 1)[1]
    user = nextUp.split(': ', 1)[0]
    print(song)
    print(user)
    uTube = youtube()
    return uTube.playSong(song)



def respond(voiceData):
    # botname = jsonifySettings.readSpecificSetting('settings.json', 'botName')
    global botname
    test_bool = False
    # if not voiceData:
    #     jsonifySettings.writeSpecificSetting('settings.json', 'speaking', 0)
    if voiceData:
        diffed_command = eval_command_ratio(voiceData.lower())
        print(diffed_command)
        if diffed_command:
            if f"{botname} play youtube" == diffed_command[:19]:
                print('playing yt')
                casePlayYoutube(voiceData)
            elif f"{botname} play requests" == diffed_command:
                casePlayRequests(voiceData)
            elif "set name" == diffed_command:
                setBotName()
            else:
                print('Waiting for command')
                jsonifySettings.writeSpecificSetting('settings.json', 'speaking', 0)


def received_yt():
    global now_time, yt_video_seconds
    if now_time and yt_video_seconds is not None:
        return True
    else:
        return False



def Main():
    global now_time
    with sr.Microphone() as source:
        secs = 5
        calibration_msg = f"Please wait for {secs} to calibrate microphone"
        print(calibration_msg)
        # listen for 5 seconds and create the ambient noise energy level
        r.adjust_for_ambient_noise(source, duration=5)
        print("Calibration complete")

        r.dynamic_energy_threshold = True
    while True:
        voiceData = record_audio()
        respond(voiceData)
        sched = threading.Thread(scheduler)
        sched.start()


def on_release(key):    # any key you want
    if key == Key.delete:
        if driver:
            driver.get('https://www.youtube.com')
    if key == Key.home:
        if driver:
            click_play_button()


with Listener(on_release=on_release) as listener:
    Main()
    listener.join()