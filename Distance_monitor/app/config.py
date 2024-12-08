# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SERIAL_PORT = os.environ.get('SERIAL_PORT') or 'COM5'  # Change as needed
    BAUD_RATE = 9600
    MAX_DATA_POINTS = 50
