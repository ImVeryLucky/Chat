from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from ai_interface import Ai_Helper
from ai_interface import create_schedule

app = Flask(__name__, template_folder="templates")
CORS(app)
global ai_instance
ai_instance = None
global first_words
first_words = None


@app.route('/')
def start():
    return render_template('index.html')

#currentHtml = 'index.html'

@app.route('/', methods = ['POST'])
def home_post():
    global ai_instance
    global first_words
    if 'start' in request.form:
        #currentHtml = 'schedule.html'
        return render_template('schedule.html', name = None, gender = None, schedule = None)
     #Back buttons
    if 'switchButton2' in request.form:
        return render_template('index.html', name = None, gender = None, schedule = None)
    if 'switchButton3' in request.form:
        return render_template('schedule.html', name = None, gender = None, schedule = None)
    
    if 'scheduler' in request.form:
        name = request.form['name']
        gender = request.form['gender']
        schedule = request.form['schedule']
        print([item.strip("\r") for item in schedule.split("\n")])
        try:
            ai_instance = Ai_Helper(
                create_schedule([item.strip("\r") for item in schedule.split("\n")]),
                                    name)
            output = ai_instance.re_input()
        except Exception as e:
            print("ERROR IN INITIATING AI")
            print(e)
            return render_template('schedule.html', name=name, gender=gender, schedule=schedule)
        return render_template('ai.html', output = output)
    
    if 'prompter' in request.form:
        prompt = request.form['promptmsg']
        print(prompt)
        output = ai_instance.talk(prompt)
        danger = False
        if output == "ERROR! Notify an assistant.":
            danger = True
        return render_template('ai.html', output=output,
                               buttonOff = danger)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)




#counter = 0  # Initial counter value
#user_input = ""
"""

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/', methods = ['POST'])
def home_post():
    if 'switchButton' in request.form:
        return render_template('2nd.html')
    if 'switchButton2' in request.form:
        return render_template('index.html', respones = None)
    data = request.form['userIn']
    return render_template('index.html', response = data)


@app.route('/update', methods=['POST'])
def update_button():
    global counter
    print("clicked")
    counter += 1
    return jsonify({"count": counter})

@app.route('/get_count', methods=['GET'])
def get_count():
    return jsonify({"count": counter})

@app.route('/process', methods=['POST'])
def process():
    global user_input
    data = request.form['userIn']
    #user_input = data.get("text")  
   #response_text = f"You entered: {user_input}" 
    return render_template('index.html', response = data)



#@app.route('/fetch', methods=['GET'])
#def fetch():    
#    return jsonify({"response": user_input})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)  # Render runs on port 10000"""