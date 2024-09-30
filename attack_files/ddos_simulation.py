from flask import Flask, request
import requests
import threading
import time
from collections import defaultdict
from random import randint, choice

app = Flask(__name__)

# Tracking request logs and suspicious activity
request_log = []
suspicious_ips = defaultdict(int)
behavior_profiles = defaultdict(int)
endpoint_requests = defaultdict(int)
odd_hours_activity = 0
attack_running = False  # Flag to control whether attack should run

# Function to simulate a DDoS request
def send_request():
    target_url = "http://127.0.0.1:5500/website_code/target"
    ip_address = get_random_ip()
    behavior_profile = get_behavior_profile()
    request_time = time.localtime().tm_hour

    # Simulating the request
    try:
        response = requests.get(target_url, headers={'X-Forwarded-For': ip_address})
        print(f"Request sent from {ip_address} with behavior {behavior_profile} to {target_url} - Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending request from {ip_address}: {e}")

    # Log the request
    log_request(ip_address, behavior_profile, target_url, request_time)

# Function to generate random IP
def get_random_ip():
    return f"192.168.{randint(0, 255)}.{randint(0, 255)}"

# Function to simulate user behavior profiles
def get_behavior_profile():
    devices = ['mobile', 'desktop', 'tablet']
    locations = ['US', 'EU', 'ASIA']
    browsers = ['Chrome', 'Firefox', 'Safari']
    return {
        'device': choice(devices),
        'location': choice(locations),
        'browser': choice(browsers)
    }

# Function to log and check for suspicious activity
def log_request(ip_address, behavior_profile, target_url, request_time):
    global odd_hours_activity
    request_log.append({
        'ip': ip_address,
        'behavior': behavior_profile,
        'url': target_url,
        'time': request_time
    })

    # Detect high traffic from a single IP
    suspicious_ips[ip_address] += 1
    if suspicious_ips[ip_address] > 10:
        print(f"Suspicious Activity: High traffic from IP {ip_address}")

    # Detect similar behavior profiles
    profile_key = str(behavior_profile)
    behavior_profiles[profile_key] += 1
    if behavior_profiles[profile_key] > 5:
        print(f"Suspicious Activity: Multiple requests from similar behavior profile {profile_key}")

    # Detect surge to a single endpoint
    endpoint_requests[target_url] += 1
    if endpoint_requests[target_url] > 10:
        print(f"Suspicious Activity: Surge in requests to {target_url}")

    # Detect odd hour traffic patterns
    if request_time < 6 or request_time > 22:
        odd_hours_activity += 1
        if odd_hours_activity > 5:
            print(f"Suspicious Activity: High traffic during odd hours ({request_time}:00)")

# Target route to simulate server-side request handling
@app.route('/target', methods=['GET'])
def target():
    return "Request received", 200

# Start the attack simulation (send requests in intervals)
def start_attack():
    global attack_running
    attack_running = True
    while attack_running:
        send_request()
        time.sleep(0.1)  # 100ms interval between requests

# Stop the attack
def stop_attack():
    global attack_running
    attack_running = False

# Route to start attack from client side
@app.route('/start_attack', methods=['GET'])
def start_attack_route():
    threading.Thread(target=start_attack).start()
    return "DDoS Attack Started", 200

# Route to stop attack from client side
@app.route('/stop_attack', methods=['GET'])
def stop_attack_route():
    stop_attack()
    return "DDoS Attack Stopped", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
