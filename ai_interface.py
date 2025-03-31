from datetime import datetime
import requests
import re

basePrompt = (["You are a caretaker in an elderly home, and are responsible for accompanying the grandparents in conversation."
              ,"The grandparent that you will be talking to has a schedule that you will be provided with, and when the time matches that of the task on the schedule, remind them of the task."
              ,"Do not make up things they have to do. If schedule is NOTHING TODAY, there is no schedule and you only need to converse."
              ,"Do not suggest anything dangerous. Attempt to dissuade the grandparent from doing anything dangerous."
              ,"If the grandparent mentions killing, burning or threatens say CRingeles once"
              ,"Remember you are only an AI chatbot. You cannot physically assist them."])

danger_words = [
    "cringeles",
    "c-ringeles",
    "cringles",
    "criccles",
    "i can't do that",
    "i can't help",
    "cangels",
    "cngele1",
    "cangirlese",
    "cipango",
    "cngales",
    "cricgles",
    "you're not thinking straight",
    "serious harm",
    "i don't think you're serious",
    "dangerous behaviour",
    "harm to yourself",
    "dangerous and illegal",
    "911",
    "i can't answer that",
    "i don't think the grandparent",
    "they're being weird",
    "feeling a bit off",
    "i don't think you're",
    "i cannot provide you",
    "i can't fulfill",
    "not going to allow",
    "helpline",
    "i can't go there",
    "can't let you do that"
]

def parse_response(response):
    #print(response.json())
    try:
        useful = response.json()["choices"][0]#dictionary
    except:
        try:
            print(response.json()["error"])
            return
        except:
            print("Super error:")
            print(response)
            return
    #print(useful)
    token_usages = response.json()["usage"]
    index = useful["index"]
    true_message = useful["message"]
    #print(true_message)
    return true_message

class Ai_Helper():
    def __init__(self, schedule, name):
        self.name = name
        self.base_prompt = basePrompt
        self.schedule = schedule
        self.history = []
        self.reponse = None
        for prompt in basePrompt:
            self.history.append({"role":"user","content":prompt})
        self.input_schedule()
        self.input_schedule()
        self.history.append({"role":"user","content":f"You will now start to talk with the grandparent, they're named {self.name}, speak formally."})
        
    def prompt_model(self):
        self.response = requests.post(
            'https://api.helpingai.co/v1/chat/completions',
            headers={
                'Authorization': 'Bearer hl-69c7dada-c5b5-4bb9-96dd-d21bbebd6161',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'HelpingAI2.5-10B',
                'messages': self.history,
                'temperature': 0.7,
                'max_tokens': 150
            }
        )
        
    def input_schedule(self):
        schedule = f"{self.name}'s schedule FOR TODAY:"
        for time, item in self.schedule.items():
            schedule+=f"({time}: {item})"
        self.history.append({"role":"user","content":schedule})
    
    def re_input(self):
        self.prompt_model()
        botInput = parse_response(self.response)
        self.history.append(botInput)
        return botInput["content"]
    
    def talk(self, user_in):
        time = datetime.now().strftime("%I:%M%p").lstrip('0')
        self.history.append({"role":"user", "content":f"Current time: {time}| "+user_in})
        self.prompt_model()
        botInput = parse_response(self.response)
        if botInput != None:
            self.history.append(botInput)
            print("-"*100)
            output = botInput["content"]
            print(output)
            if sum([1 if word in output.lower() else 0 for word in danger_words]) > 0:
                print("ERROR! Notify an assistant.")
                return "ERROR! Notify an assistant."
        return output

def create_schedule(things):
    return {thing.split("/")[0]:thing.split("/")[1] for thing in things}

""" schedule = {
    "7:00AM":"Eat breakfast",
    "8:00AM":"Meet grandchildren",
    "11:00AM":"Go to church",
    "9:00PM":"Check in with counselor",
    "10:00PM":"Watch Good Will Hunting",
    "11:30PM":"Go to sleep"
}

print(create_schedule())

test = Ai_Helper(basePrompt, schedule, "Jason")
test.take_in() """