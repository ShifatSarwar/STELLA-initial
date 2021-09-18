import listen
import communicate
import changeVoice
import playFromYouTube
import datetime
import programExit
#checking import

if __name__ == '__main__':
    communicate.setValueID(communicate.getValueID())
    command = listen.startListening()

    if('stella' in command):
        communicate.speak("Hi, Shifat")
        #While loop iterates as long as None data or user says exit
        while('exit' not in command):
            if('change voice' in command): 
                changeVoice.vChange(0)
            elif('play' in command):
                videoTitle= command.replace('play', '')
                print(videoTitle)
                communicate.speak("Playing "+ videoTitle)
                playFromYouTube.play(videoTitle)
            elif('time' in command):
                time = datetime.datetime.now().strftime('%I:%M:%p')
                communicate.speak("The current time is, " + time)
                programExit.sExit()
            else:
                communicate.speak("How can I help you?")
                command = listen.startListening()  
        communicate.speak("okay") 
        programExit.pExit()     
    elif("exit" in command):
        communicate.speak("okay") 
        programExit.pExit()
    else:
        command = listen.startListening()


    


