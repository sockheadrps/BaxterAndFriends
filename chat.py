import socket
from gtts import gTTS
import playsound
import os
import jsonifySettings
import datetime as dt
import timer
import threading
import pickle

# read white list users
def read_white_list():
    try:
        white_list = pickle.load(open('whiteList.p', 'rb'))
        return white_list
    except:
        print('No white list!')

def add_user_to_white_list(user_to_add):
    wl_users = read_white_list()
    wl_users.append(user_to_add)
    pickle.dump(wl_users, open("whiteList.p", "wb"))


discord_link = r'https://discord.gg/zar9q45'
soundPath = jsonifySettings.readSpecificSetting('settings.json', 'soundFolderLocation')
soundBlocker = False 

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = jsonifySettings.readSpecificSetting('settings.json', 'oAuth')
BOT = "TwitchBot"
CHANNEL = jsonifySettings.readSpecificSetting('settings.json', 'twitchUser')
OWNER = jsonifySettings.readSpecificSetting('settings.json', 'twitchUser')
irc = socket.socket()
irc.connect((SERVER, PORT))

# SERVER = "irc.twitch.tv"
# PORT = 6667
# PASS = jsonifySettings.readSpecificSetting('settings.json', 'oAuth')
# BOT ="TwitchBot"
# CHANNEL = "sockheadrps"
# OWNER = "sockheadrps"
# irc = socket.socket()
# irc.connect((SERVER, PORT))


irc.send((  f'PASS {PASS}\n'
            f'NICK {BOT}\n'
            f'JOIN #{CHANNEL}\n').encode())

def saveToSongRequests(songReqUser, songReqMessage):
    try:
        if songReqMessage != '!sr':
            # take input
            toSave = "{" + songReqUser + ": " + songReqMessage[3:] + '}'
            print(toSave)
            # save the info to the file
            f = open('songRequests.txt', 'a')
            f.write(toSave)
            f.write('\n')
            f.close()

    except Exception as e:
        print(e)
        print('Song Request File not initilized')

def listDir(dir):
    commandList = []
    commands = []
    fileNames = os.listdir(dir)
    for fileName in fileNames:
        fileName = fileName[:-4]
        commandList.append(fileName)
        commands.append('!' + fileName)
    return commandList, commands

def speak(text):
    maxChars = jsonifySettings.readSpecificSetting('settings.json', 'ttsMaxChars')
    for line in text:
        if not line.startswith("!"):
            txt = text[:int(maxChars)]
            tts = gTTS(text=txt, lang="en", slow=False)
            filename = "voice.mp3"
            tts.save(filename)
            playsound.playsound(filename)
            os.remove("voice.mp3")
            break

def defaultChatMessage():
    if jsonifySettings.readSpecificSetting('settings.json', 'chatMessageTimer') != 0:
        sendMessage(irc," Welcome to the Stream. Type !commands to see chat commands, use one to get my attention.")
        timer.secondTimerChatMessage(4)

def joinchat():
    loading = True
    while loading:
        print('loading...')
        readbuffer_join = irc.recv(1024)
        print('recieved')
        readbuffer_join = readbuffer_join.decode()
        print('buffer read')   
        for line in readbuffer_join.split("\n")[0:-1]:
            print(line)
            loading = loadingComplete(line)

        if loading == False:
            break
    print('Chat joined')

def loadingComplete(line):
    print(line)
    if("End of /NAMES list" in line):
        print("Bot has joined " + CHANNEL + "'s Channel!")
        sendMessage(irc, "Chat room joined!")
        return False
    else:
        return True



def sendMessage(irc, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    irc.send((messageTemp + "\n").encode())

def getUser(line):
    seperate = line.split(":", 2)
    user = seperate[1].split("!", 1)[0]
    return user

def getMessage(line):
    try:
        message = (line.split(":", 2))[2]
    except:
        message = ""
    return message

def Console(line):
    if "PRIVMSG" in line:
        return False
    else: 
        return True


def main():
    global soundBlocker
    try:
        commands, commandList = listDir(jsonifySettings.readSpecificSetting('settings.json', 'soundFolderLocation'))
    except Exception as e:
        print(e)
        print('Sounds folder not set')
    t = dt.datetime.now()
    while True:
        delta = dt.datetime.now()-t
        if delta.seconds >= jsonifySettings.readSpecificSetting('settings.json', 'sliderFileIndicatorSoundsCoolDown') and soundBlocker == True:
            t = dt.datetime.now()
            soundBlocker = False
            print(soundBlocker)
            print(dt.datetime.now())

        
        try:
            readbuffer = irc.recv(1024).decode()
        except Exception as e:
            readbuffer = ""
            print('bufferEmpty')
            print(e)
        for line in readbuffer.split("\r\n"):
            if line == "":
                continue
    # handle if the input is a twitch ping
            elif "PING" in line and Console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send(msgg)
                print(msgg)
                continue
            else:
                user = getUser(line)
                message = getMessage(line)
                print(user + " : " + message)
                if message.lower()[0:4] == '!ftoc':
                    sendMessage(irc, 'ftoc')
                if message.lower() == '!discord':
                    sendMessage(irc, discord_link)

                if 'https' in message and '!sr' not in message:
                    speak(user + " sent a link")
                if message[:3] == '!sr':
                        print('song request recieved')
                        speak(user + ' sent a song request')
                        saveToSongRequests(user, message)
                if message[0] != "!" and 'http' not in message:
                    if jsonifySettings.readSpecificSetting('settings.json', 'ttsSetting'):
                        try:
                            speak(message)
                        except Exception as e:
                            print(e)
                messageLower = message.lstrip().lower()
                print(soundBlocker)
                print(delta.seconds)
                if delta.seconds <= jsonifySettings.readSpecificSetting('settings.json', 'sliderFileIndicatorSoundsCoolDown') and soundBlocker == True:
                    sendMessage(irc," Sounds are on cooldown :).")
                if delta.seconds >= jsonifySettings.readSpecificSetting('settings.json', 'sliderFileIndicatorSoundsCoolDown') and soundBlocker == False:
                    if messageLower[0] == '!' and messageLower == '!commands':
                        print(commandList)
                        sendMessage(irc, str(commandList))
                    if messageLower[0] == '!' and messageLower != '!commands' and messageLower[0:3] != "!sr":
                        for thing in commands:
                            print(messageLower[1:])
                            if messageLower[1:] in thing:
                                print('found sound commands...')
                                print('sound setting at message if statement' + str(soundBlocker))
                                if jsonifySettings.readSpecificSetting('settings.json', 'soundSetting') == 1:
                                    try:
                                        t = dt.datetime.now()
                                        soundBlocker = True
                                        sound = soundPath + messageLower[1:]+'.mp3'
                                        playsound.playsound(soundPath + messageLower[1:]+'.mp3', block = False)
                                    except Exception as e:
                                        print(e)
                                break


        if jsonifySettings.readSpecificSetting('settings.json', 'chatRunning') == 0:    
            print('chatRunning setting is 0')
            exit()




if __name__ == '__main__':
    joinchat()
    main()
