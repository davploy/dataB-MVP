from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)

# Configure CORS more explicitly
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5000", "http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/input', methods=['POST'])
def inputs():
    csv_data = request.data.decode('utf-8')
    print(csv_data)
    return {'status': 'received'}

if __name__ == '__main__':
    app.run(debug=True, port=5000)