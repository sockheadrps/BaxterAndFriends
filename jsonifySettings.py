import json
import threading

json_lock = threading.Lock()
def writeSettings(jsonFile, settingsDict):
    j = json.dumps(settingsDict)
    with open(jsonFile, 'w') as f:
        f.write(j)
        f.close()

def readSettings(jsonFile):
    read = json.load(open(jsonFile))
    # returns a dict
    return read

def writeSpecificSetting(jsonFile, settingName, settingVal):
    settingsDict = readSettings(jsonFile)
    settingsDict[settingName] = settingVal
    writeSettings(jsonFile, settingsDict)

def readSpecificSetting(jsonFile, settingName):
    settingsDict = None
    while settingsDict is None:
        try:
            settingsDict = readSettings(jsonFile)
        except Exception as e:
            print(e)
    settingVal = settingsDict[settingName]
    writeSettings(jsonFile, settingsDict)
    return settingVal


# Initializing files, if not in directory
settingsFile = 'settings.json'

try:
    open(settingsFile, 'r')
except:  
    sets = {
        'oAuth' :  '',
        'ytApiKey' : '',
        'twitchUser' : '',
        'twitchPass' : '',
        'chatRunning' : 0,
        'sliderFileIndicatorSoundsCoolDown' : 0,
        'soundSetting' : 0,
        'ttsSetting' : 0,
        'ttsMaxChars' : 0,
        'chatMessageTimer' : 10,
        'soundFolderLocation' : '',
        'botName' : 'bot', "robot"
        'killYT' : 0,
        'autoPlaySR' : 0,
        'speaking' : 0,
        'baxterRunning' : 0

    }
    writeSettings(settingsFile, sets)
