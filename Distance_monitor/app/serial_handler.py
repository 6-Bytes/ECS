# app/serial_handler.py
import serial
import threading
import time
from app.config import Config

class SerialHandler:
    def __init__(self):
        self.sensor_data = {
            "sensor1": 0,
            "sensor2": 0,
            "timestamp": 0
        }
        self.serial_port = None
        self._start_serial_connection()

    def _start_serial_connection(self):
        try:
            self.serial_port = serial.Serial(Config.SERIAL_PORT, Config.BAUD_RATE)
            # Start reading thread
            thread = threading.Thread(target=self._read_serial, daemon=True)
            thread.start()
        except Exception as e:
            print(f"Error initializing serial connection: {e}")

    def _read_serial(self):
        while True:
            try:
                if self.serial_port and self.serial_port.in_waiting:
                    line = self.serial_port.readline().decode('utf-8').strip()
                    if "Sensor 1 Distance:" in line:
                        parts = line.split("|")
                        sensor1 = float(parts[0].split(":")[1].strip().replace(" cm", ""))
                        sensor2 = float(parts[1].split(":")[1].strip().replace(" cm", ""))
                        
                        self.sensor_data["sensor1"] = sensor1
                        self.sensor_data["sensor2"] = sensor2
                        self.sensor_data["timestamp"] = time.time()
            except Exception as e:
                print(f"Error reading serial: {e}")
                time.sleep(1)

    def get_data(self):
        return self.sensor_data

# Create a singleton instance
serial_handler = SerialHandler()

def get_sensor_data():
    return serial_handler.get_data()