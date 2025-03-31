from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

counter = 0  # Initial button state

@app.route('/update', methods=['POST'])
def update_button():
    global counter
    counter += 1  # Increase counter
    return jsonify({"count": counter})

@app.route('/get_count', methods=['GET'])
def get_count():
    return jsonify({"count": counter})

if __name__ == '__main__':
    app.run(debug=True)
