# BaxterAndFriends
Python Version 3.7.1  
A series of tools for steaming on Twitch.tv  

Current Features:  
  Web interface  
    -A web page with a series of inputs (buttons and sliders) to adjust settings.  
      Buttons  
        -TTS On/Off  
        -Stream Sound clips On/Off  
        -Auto Play Song Requests On/Off  
        -Start/Stop Baxter  
        -Connect/Disconnect from Twitch Chat  
       Sliders  
        -Cooldown adjustment for stream sounds  
        -TTS max characters to read from Twitch chat         
        
  Voice Recognition
    -"Baxter Play Requests"
      -Plays the next song request in queue, if one exists
    -"Baxter Play youtube <Video title to play>
      -This will search and play the first video found with your Video description used as a query on YouTube.
  
  On Screen Web Pages as Stream Widgets:
    These "widgets" are generated webpages that can be used to display dynamic information in StreamLabs (or similiar software) as a         brwoser source
      -Now Playing
        -Displays the video title from the songsRequest file and the user that requested it, as well as the next video and user in                queue. These songs are played through the same automated browser actions as 'Play Youtube' that the voice recognition uses.
  
  
  On first run:
  1. Install PyAudio wheel included in BaxterAndFriends dir, and other library requirements.
  2. Run jsonifySettings.py - This creates a file called settings.json with some parameters we will fill in with the GUI.
  3. Run open a cmd prompt from the BaxterAndFriends folder and open app.py with python
  4. On the GUI, click Configure and paste in the location of the sounds directory (in github I have included a folder with some sounds,      currently located in BaxterAndFriends/Sounds, but paste the entire path
  5. Click Confingure and enter in the remaining the necessary data. (Twitch Oauth, Login info, YoutTube API key)
  6. Click file and click scan sounds (ensure you do this after completing the configure step)
  7. Set up is complete, you can use the app.
