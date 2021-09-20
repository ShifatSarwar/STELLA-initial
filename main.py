from torch.nn.modules.activation import Softmax
import listen
import communicate
import changeVoice
import playFromYouTube
import datetime
import random
import torch
import json
from model import NeuralNet
from answerSmart import tokenize, bag_of_words
import programExit
#checking import

if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    with open('intents.json', 'r') as json_data:
       intents = json.load(json_data) 

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    communicate.setValueID(communicate.getValueID())

    while True:
        command = listen.startListening()
        if 'exit' in command:
            programExit.pExit()

        elif('change voice' in command):
            changeVoice.vChange(0)

        elif('time' in command):
            time = datetime.datetime.now().strftime('%I:%M:%p')
            communicate.speak("The current time is, " + time)
        else:
            command = tokenize(command)
            X = bag_of_words(command, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted  = torch.max(output, dim=1)

            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
        
            if prob.item() > 0.75 :
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        response = random.choice(intent["responses"])
                        if tag == "youtube":
                            for tokens in intent["patterns"]:
                                if tokens in command:
                                    command.remove(tokens)
                            videoTitle = ' '.join(command)
                            print(videoTitle)
                            communicate.speak(response+videoTitle)
                            playFromYouTube.play(videoTitle)
                        else:
                            communicate.speak(response)
                        
            else:
                communicate.speak("Sorry, could not understand you")
  
        

            




