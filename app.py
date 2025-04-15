from flask import Flask, render_template, jsonify, request
import time
from datetime import datetime

app = Flask(__name__)

# Mock data for demonstration
def get_mock_alerts():
    return [
        {"id": 1, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "type": "Port Scan", "source": "192.168.1.100", "severity": "High"},
        {"id": 2, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "type": "SQL Injection", "source": "10.0.0.5", "severity": "Critical"},
        {"id": 3, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "type": "Brute Force", "source": "172.16.0.1", "severity": "Medium"}
    ]

def get_mock_traffic():
    return {
        "total_packets": 1500,
        "blocked_packets": 50,
        "allowed_packets": 1450,
        "alerts": 3
    }

# Store settings in memory (in a real app, this would be in a database)
threshold_settings = {
    "max_packets": 1000,
    "max_connections": 50
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/api/status')
def get_status():
    # Simplified status check without psutil
    return jsonify({
        "snort_status": "Running",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "system_status": "Normal",
        "uptime": "1h 23m"
    })

@app.route('/api/alerts')
def get_alerts():
    return jsonify(get_mock_alerts())

@app.route('/api/traffic')
def get_traffic():
    return jsonify(get_mock_traffic())

@app.route('/api/settings', methods=['GET', 'POST'])
def handle_settings():
    global threshold_settings
    
    if request.method == 'POST':
        data = request.get_json()
        threshold_settings.update({
            "max_packets": data.get('max_packets', 1000),
            "max_connections": data.get('max_connections', 50)
        })
        return jsonify({"message": "Settings updated successfully", "settings": threshold_settings})
    
    return jsonify(threshold_settings)

if __name__ == '__main__':
    app.run(debug=True) 