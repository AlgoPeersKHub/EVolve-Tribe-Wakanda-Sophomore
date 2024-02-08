

import network
import machine
import time
import socket

# Define pins for the Hall effect sensor and wind vane position sensor (potentiometer)
hall_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)  # Example pin for Hall effect sensor, adjust as necessary
position_pin = machine.Pin(15, machine.Pin.IN)  # Example pin for position sensor, adjust as necessary

# Constants
CIRCUMFERENCE = 0.2  # Circumference of the circle described by the cups in meters
SECONDS_PER_MINUTE = 60  # Number of seconds in a minute

# Wi-Fi credentials
WIFI_SSID = "Your WiFi SSID"
WIFI_PASSWORD = "Your WiFi Password"

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Wi-Fi connected")
    print("IP Address:", wlan.ifconfig()[0])

def calculate_wind_speed(pulse_count, time_interval):
    rotations_per_second = pulse_count / time_interval
    wind_speed_mps = rotations_per_second * CIRCUMFERENCE
    return wind_speed_mps

def read_wind_direction(position_pin):
    # Read analog value from position sensor (potentiometer)
    analog_value = position_pin.read_u16()  # Assuming position sensor provides analog values (adjust as necessary)
    # Convert analog value to wind direction (example calibration)
    # You may need to adjust this calibration based on your specific setup
    wind_direction_degrees = analog_value * 360 / 65535  # Convert analog value to degrees (0-360)
    return wind_direction_degrees

def main():
    connect_to_wifi()
    
    pulse_count = 0
    last_time = time.time()

    # Define the IP address and port for this Raspberry Pi
    local_ip = "192.168.1.100"  # Adjust as necessary
    port = 12345  # Adjust as necessary

    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((local_ip, port))
    s.listen(1)

    print("Waiting for connection...")
    conn, addr = s.accept()
    print("Connected to:", addr)

    while True:
        # Read state of the Hall effect sensor
        hall_state = hall_pin.value()
        
        # If the state has changed (i.e., a magnet passed by)
        if hall_state == 0:  # Assuming the sensor is triggered by a falling edge
            pulse_count += 1
        
        # Measure time elapsed
        current_time = time.time()
        time_interval = current_time - last_time
        
        # Update last time
        last_time = current_time
        
        # Calculate wind speed every minute
        if time_interval >= SECONDS_PER_MINUTE:
            wind_speed = calculate_wind_speed(pulse_count, time_interval)
            wind_direction = read_wind_direction(position_pin)
            data = "Wind Speed: {:.2f} m/s\nWind Direction: {:.2f} degrees\n".format(wind_speed, wind_direction)
            conn.sendall(data)
            print("Data sent to smartphone")
            
            # Reset pulse count and timer
            pulse_count = 0
            last_time = time.time()
            
        time.sleep(0.1)  # Adjust sleep time as necessary to avoid high CPU usage

if __name__ == "__main__":
    main()


