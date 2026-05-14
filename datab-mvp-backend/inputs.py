from flask import Flask, request
from flask_cors import CORS

from llm import CSVAnalyzer

app = Flask(__name__)
analyzer = CSVAnalyzer()

# Configure CORS more explicitly
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:5000",
            "http://localhost:5173",
            "http://localhost:5174",
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/input', methods=['POST'])
def inputs():
    """Debug endpoint: echo back the CSV data."""
    csv_data = request.data.decode('utf-8')
    print(csv_data)
    return {'status': 'received'}

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze CSV data using Anthropic Claude."""
    try:
        csv_text = request.data.decode('utf-8')

        if not csv_text or not csv_text.strip():
            return {'status': 'error', 'message': 'Empty CSV'}, 400

        result = analyzer.analyze(csv_text)
        return {'status': 'success', 'result': result}

    except Exception as e:
        import traceback
        print(f"ERROR in /analyze: {str(e)}", flush=True)
        print(traceback.format_exc(), flush=True)
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)