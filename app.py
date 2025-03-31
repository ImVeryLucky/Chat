from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)

counter = 0  # Initial counter value

@app.route('/')
def home():
    return render_template('index.html')  # Serve frontend

@app.route('/update', methods=['POST'])
def update_button():
    global counter
    counter += 1
    return jsonify({"count": counter})

@app.route('/get_count', methods=['GET'])
def get_count():
    return jsonify({"count": counter})

@app.route('/process', methods=['POST'])
def process():
    data = request.json  
    user_input = data.get("user_input", "")  
    response_text = f"You entered: {user_input}" 
    return jsonify({"response": response_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)  # Render runs on port 10000