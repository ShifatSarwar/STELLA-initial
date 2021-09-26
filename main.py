#!/usr/bin/env python
from torch.nn.modules.activation import Softmax
import listen
import communicate
#import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageSequence 
from calculations import addition, subtraction, division, multiplication, tothePower, percentages
import changeVoice
from variousSearch import googleSearch, play, findInfo, chooseGenre
import datetime
import random
import torch
import programExit
import json
from model import NeuralNet
from nltkutilities import tokenize, bag_of_words
#checking import

if __name__ == '__main__':

    #Allows use of cuda or cpu for computing prediction
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    #read from json data for getting responses based on asked questions
    with open('intents.json', 'r') as json_data:
       intents = json.load(json_data) 

    #File contains model trained
    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    #Gets model up and running
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    #loads up chosen voice rather than default voice
    communicate.setValueID(communicate.getValueID())

  ##  sg.theme('DarkAmber')
  ## gif_filename = r'shapeB.gif'

  ##  layout = [[ 
  ##  [sg.Image(filename=gif_filename,
   #           enable_events=True,
    #          key="-IMAGE-")],

   # ]]

    # Create the Window
    #window = sg.Window('STELLA', layout, finalize=True) 
    
    #listening starts here
    while True:
        command = listen.startListening()
     #   for frame in ImageSequence.Iterator(Image.open(gif_filename)):
      #      event, values = window.read(timeout=10)
       #     window['-IMAGE-'].update(data=ImageTk.PhotoImage(frame) )
        if 'exit' in command or 'go away' in command:
            break

        elif('change voice' in command):
            changeVoice.vChange()

        elif('time' in command):
            time = datetime.datetime.now().strftime('%I:%M:%p')
            communicate.speak("The current time is, " + time)
        else:
            #convert command into a tokenized array
            command = tokenize(command)

            #get arrays to compare and predict
            X = bag_of_words(command, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted  = torch.max(output, dim=1)

            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]

            #runs if probability high
            if prob.item() > 0.75 :
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        response = random.choice(intent["responses"])
                        
                        if tag == "youtube":
                            #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                if tokens in command:
                                    command.remove(tokens)
                            videoTitle = ' '.join(command)
                            communicate.speak(response+videoTitle)
                            play(videoTitle)

                        elif tag == 'search':
                        #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                if tokens in command:
                                    command.remove(tokens)
                            search = ' '.join(command)
                            communicate.speak(response+search)
                            googleSearch(search)

                        elif tag == 'info':
                        #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                if tokens in command:
                                    command.remove(tokens)
                            searchInfo = ' '.join(command)
                            communicate.speak(response)
                            communicate.speak(findInfo(searchInfo))

                        #calculations
                        elif tag == 'add':
                            searchInfo =' '.join(command)
                            communicate.speak(response+addition(searchInfo))
                        
                        elif tag == 'subtract':
                            searchInfo =' '.join(command)
                            communicate.speak(response+subtraction(searchInfo))
                        
                        elif tag == 'multiply':
                            searchInfo =' '.join(command)
                            communicate.speak(response+multiplication(searchInfo))
                        
                        elif tag == 'divide':
                            searchInfo =' '.join(command)
                            communicate.speak(response+division(searchInfo))
                        
                        elif tag == 'percent':
                            searchInfo =' '.join(command)
                            communicate.speak(response+percentages(searchInfo))
                        
                        elif tag == 'power':
                            searchInfo =' '.join(command)
                            communicate.speak(response+tothePower(searchInfo))
                        
                        elif tag == 'suggest':
                            communicate.speak("Sorry, that is not available yet")


                        else:
                            #A response generated by AI
                            communicate.speak(response)
                    
                                
            else:
                #response if user talks jibberish
                communicate.speak("Sorry, could not understand you")

    programExit.pExit()
  
        






