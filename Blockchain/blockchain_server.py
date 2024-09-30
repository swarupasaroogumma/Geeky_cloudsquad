from flask import Flask, request, jsonify # type: ignore

app = Flask(__name__)

@app.route('/validate', methods=['POST'])
def validate():
    """Simulate sending flagged data to a blockchain."""
    data = request.json.get('data')
 
    print("Data received for validation:", data)
    return jsonify({'status': 'success', 'message': 'Data validated.'})

if __name__ == '__main__':
    app.run(port=8001)
