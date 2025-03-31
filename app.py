from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

counter = 0  # Initial counter value
user_input = ""


@app.route('/')
def home():
    return render_template('index.html')  # Serve frontend

@app.route('/update', methods=['POST'])
def update_button():
    global counter
    print("clicked")
    counter += 1
    return jsonify({"count": counter})

@app.route('/get_count', methods=['GET'])
def get_count():
    return jsonify({"count": counter})

@app.route('/', methods=['POST'])
def process():
    global user_input
    data = request.form
    user_input = data.get("text")  
   #response_text = f"You entered: {user_input}" 
    print(data)
    return None



@app.route('/fetch', methods=['GET'])
def fetch():
    return jsonify({"response": user_input})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)  # Render runs on port 10000