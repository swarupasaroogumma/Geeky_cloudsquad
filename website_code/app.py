from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import requests

app = Flask(__name__)

# Load the pre-trained autoencoder model
autoencoder = load_model('autoencoder_model.h5')

def detect_anomalies(autoencoder, data, threshold=0.1):
    """Detect anomalies in the traffic data."""
    predictions = autoencoder.predict(data)
    mse = np.mean(np.power(data - predictions, 2), axis=1)
    anomalies = mse > threshold
    return anomalies

def send_to_blockchain(data):
    """Send flagged data to a mock blockchain validation system."""
    blockchain_url = 'http://localhost:8001/validate'  # Replace with your blockchain endpoint
    response = requests.post(blockchain_url, json={'data': data.tolist()})
    return response.json()

@app.route('/analyze', methods=['POST'])
def analyze_traffic():
    """Analyze incoming traffic data for anomalies."""
    try:
        traffic_data = np.array(request.json['data'])
        
        # Detect anomalies
        anomalies = detect_anomalies(autoencoder, traffic_data)
        
        # If anomalies are detected, send them to the blockchain
        if np.any(anomalies):
            flagged_data = traffic_data[anomalies]
            blockchain_response = send_to_blockchain(flagged_data)
            return jsonify({'status': 'success', 'flagged_data': flagged_data.tolist(), 'blockchain_response': blockchain_response})
        else:
            return jsonify({'status': 'success', 'message': 'No anomalies detected.'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
