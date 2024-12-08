from flask import Flask, render_template, jsonify 
import serial
import threading
import time
import json

app = Flask(__name__)

# Global variables to store the latest sensor readings
sensor_data = {
    "sensor1": 0,
    "sensor2": 0,
    "timestamp": 0
}

def read_serial():
    """Background thread function to continuously read from Arduino"""
    # Update these settings according to your system
    ser = serial.Serial('COM5', 9600)  # Change COM3 to your Arduino port
    
    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                # Parse the line to extract distances
                if "Sensor 1 Distance:" in line:
                    parts = line.split("|")
                    sensor1 = float(parts[0].split(":")[1].strip().replace(" cm", ""))
                    sensor2 = float(parts[1].split(":")[1].strip().replace(" cm", ""))
                    
                    # Update global sensor_data
                    sensor_data["sensor1"] = sensor1
                    sensor_data["sensor2"] = sensor2
                    sensor_data["timestamp"] = time.time()
        except Exception as e:
            print(f"Error reading serial: {e}")
            time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    return jsonify(sensor_data)

# Create the templates directory and index.html file
import os
if not os.path.exists('templates'):
    os.makedirs('templates')

with open('templates/index.html', 'w') as f:
    f.write('''
<!DOCTYPE html>
<html>
<head>
    <title>Distance Monitor</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        .sensor-reading { 
            padding: 20px;
            margin: 10px 0;
            background-color: #f0f0f0;
            border-radius: 5px;
        }
        canvas { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Distance Monitor</h1>
        <div class="sensor-reading">
            <h2>Current Readings</h2>
            <p>Sensor 1: <span id="sensor1">--</span> cm</p>
            <p>Sensor 2: <span id="sensor2">--</span> cm</p>
        </div>
        <canvas id="distanceChart"></canvas>
    </div>

    <script>
        // Initialize the chart
        const ctx = document.getElementById('distanceChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Sensor 1',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }, {
                    label: 'Sensor 2',
                    data: [],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Distance (cm)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    }
                }
            }
        });

        // Update data every 100ms
        const maxDataPoints = 50;
        setInterval(() => {
            fetch('/data')
                .then(response => response.json())
                .then(data => {
                    // Update current readings
                    document.getElementById('sensor1').textContent = data.sensor1.toFixed(1);
                    document.getElementById('sensor2').textContent = data.sensor2.toFixed(1);

                    // Update chart
                    const timestamp = new Date().toLocaleTimeString();
                    chart.data.labels.push(timestamp);
                    chart.data.datasets[0].data.push(data.sensor1);
                    chart.data.datasets[1].data.push(data.sensor2);

                    // Remove old data points if we have too many
                    if (chart.data.labels.length > maxDataPoints) {
                        chart.data.labels.shift();
                        chart.data.datasets[0].data.shift();
                        chart.data.datasets[1].data.shift();
                    }

                    chart.update();
                });
        }, 100);
    </script>
</body>
</html>
    ''')

if __name__ == '__main__':
    # Start the serial reading thread
    serial_thread = threading.Thread(target=read_serial, daemon=True)
    serial_thread.start()
    
    # Start the Flask application
    app.run(debug=True)