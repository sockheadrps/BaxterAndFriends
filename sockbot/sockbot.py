import speech_recognition as sr
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import urllib
import urllib.request
from time import sleep


apiKey = 'AIzaSyBKI-4e-bFE_iIK8ZWU5hwv9lGoZCYuTvU'
r = sr.Recognizer()

class youtube():
    def __init__(self):
        print('Playing youtube video...')

    def playSong(self, search):
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 3)
        presence = EC.presence_of_element_located
        visible = EC.visibility_of_element_located    
        # Navigate to url with video being appended to search_query
        driver.get("https://www.youtube.com/results?search_query=" + str(search.replace(" ", '+')))
        print(driver.current_url)

        # play the video
        wait.until(visible((By.ID, "video-title")))
        driver.find_element_by_id("video-title").click()



def getYoutubeVidDuration(videoLink):
    videoId = videoLink.split('=',1)[1]
    searchUrl="https://www.googleapis.com/youtube/v3/videos?id="+videoId+"&key="+apiKey+"&part=contentDetails"
    print(searchUrl)
    response = urllib.request.urlopen(searchUrl).read()
    data = json.loads(response)
    all_data=data['items']
    contentDetails=all_data[0]['contentDetails']
    duration=contentDetails['duration']
    print(duration)
    minutes = duration.split('M',1)[0]
    minutes = minutes[2:]
    seconds = duration.split('M',1)[1]
    seconds = seconds[:2]
    return(minutes, seconds)

def setBotName():
    botNames = []
    for x in range(3):
        print('Speak your bot name')
        botNames.append(record_audio())
        print(botNames)
    return botNames

def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            print(ask)
        audio = r.listen(source)
        try:
            voiceData = r.recognize_google(audio)
            print(voiceData)
            return voiceData

        except sr.UnknownValueError:
            print('Sorry I didnt get that')
        except sr.RequestError:
            print('Voice service is down')

def respond(voiceData):
    try:
        if 'what is your name' in voiceData:
            print('my name is sock bot')
        if 'play youtube' in voiceData.lower():
            toSearch = voiceData.lower()[11:]
            uTube = youtube()
            uTube.playSong(toSearch)
            print(toSearch)
        else:
            print('Waiting for command')
    except Exception as e:
        print(e)

def main():
    # setBotName()
    while True:
        voiceData = record_audio()
        respond(voiceData)
    # print(getYoutubeVidDuration('https://www.youtube.com/watch?v=ZkYOvViSx3E&list=PL5tcWHG-UPH29oYVpxP4B-boItTS7n49G&index=2'))


if __name__ == '__main__':
    main()
