import speech_recognition as sr
import programExit
listener = sr.Recognizer()
mic= sr.Microphone()

def startListening():
     
    with mic as source:

        print("............")
        listener.adjust_for_ambient_noise(source)
        audioData = listener.listen(source)
        
        response = {
            "success": True,
            "error": None,
            "voicedata": ""
        }

        try:
            response["voicedata"] = listener.recognize_google(audioData)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "can't reach google"
        except sr.UnknownValueError:
            response["error"] = "couldn't hear you"
        if(response["success"] == True):
            print(response["voicedata"])
            return (response["voicedata"]).lower()
        else:
            print(response["error"])
            programExit.pExit()
        
