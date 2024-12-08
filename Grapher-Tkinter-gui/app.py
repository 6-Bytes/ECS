import tkinter as tk
from tkinter import ttk
import serial
import time
from serial.tools import list_ports

class RadarGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Ultrasonic Radar System")
        self.master.geometry("800x400")
        self.master.configure(bg='black')

        # Create main frame
        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Create canvas for radar display
        self.canvas = tk.Canvas(self.main_frame, width=600, height=200, bg='black')
        self.canvas.pack(pady=20)

        # Initialize radar display elements
        self.create_radar_display()

        # Status label
        self.status_label = tk.Label(self.main_frame, text="Status: Connecting...", 
                                     fg="white", bg="black")
        self.status_label.pack(pady=10)

        # Connect to Arduino
        self.connect_to_arduino()

        # Start updating the display
        self.update_radar()

    def create_radar_display(self):
        # Create radar lines
        for i in range(1, 21):
            x1 = 100
            y1 = 200 - i * 10
            x2 = 600
            y2 = 200 - i * 10
            self.canvas.create_line(x1, y1, x2, y2, fill='green', width=1)

        # Create range labels
        ranges = [100, 500, 1000, 1500, 1999]
        for i, range_val in enumerate(ranges):
            y_pos = 200 - (i + 1) * 10 - 10
            self.canvas.create_text(50, y_pos, text=f"{range_val}cm", 
                                    fill='green', anchor='e')

        # Create detection zone
        self.detection_zone = self.canvas.create_rectangle(100, 0, 600, 200, 
                                                          outline='darkgreen', 
                                                          fill='', width=2)

        # Create detection indicator
        self.distance_indicator = self.canvas.create_text(550, 180, text="Distance: 0 cm", 
                                                          fill='white')

    def connect_to_arduino(self):
        try:
            # Automatically find Arduino port
            ports = list_ports.comports()
            for port in ports:
                if 'Arduino' in port.description or 'CH340' in port.description:
                    self.arduino = serial.Serial(port.device, 9600, timeout=1)
                    self.status_label.config(text=f"Connected to Arduino on {port.device}")
                    return
            
            # If no Arduino found, try common port names
            common_ports = ['COM5', 'COM4', '/dev/ttyUSB0', '/dev/ttyACM0']
            for port in common_ports:
                try:
                    self.arduino = serial.Serial(port, 9600, timeout=1)
                    self.status_label.config(text=f"Connected to Arduino on {port}")
                    return
                except serial.SerialException:
                    continue
            
            self.status_label.config(text="Could not connect to Arduino")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def update_radar(self):
        try:
            if hasattr(self, 'arduino') and self.arduino.is_open:
                if self.arduino.in_waiting:
                    data = self.arduino.readline().decode().strip()
                    if data.replace('.', '', 1).isdigit():  # Check if the data is a valid float
                        distance = float(data)

                        # Update radar visualization
                        self.update_detection_zone(distance)

                        # Update distance label
                        self.canvas.itemconfig(self.distance_indicator, 
                                               text=f"Distance: {distance:.1f} cm")

                        # Check for object detection
                        if 1 <= distance <= 1999:
                            self.canvas.itemconfig(self.detection_zone, fill='red')
                            self.status_label.config(text="Object Detected!")
                        else:
                            self.canvas.itemconfig(self.detection_zone, fill='')
                            self.status_label.config(text="Monitoring...")
                    else:
                        self.status_label.config(text="Invalid data received from Arduino")
            else:
                self.status_label.config(text="Waiting for Arduino connection...")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

        # Schedule next update
        self.master.after(100, self.update_radar)

    def update_detection_zone(self, distance):
        # Normalize distance to fit our display
        max_range = 1999  # maximum range in cm
        norm_distance = min(distance / max_range, 1.0)

        # Update zone size based on distance
        zone_width = 500 * norm_distance
        self.canvas.coords(self.detection_zone, 100, 0, 100 + zone_width, 200)

if __name__ == "__main__":
    root = tk.Tk()
    app = RadarGUI(root)
    root.mainloop()
