
import machine
import time
import bluetooth

# Define pins for the Hall effect sensor and wind vane position sensor (potentiometer)
hall_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)  # Example pin for Hall effect sensor, adjust as necessary
position_pin = machine.Pin(15, machine.Pin.IN)  # Example pin for position sensor, adjust as necessary

# Constants
CIRCUMFERENCE = 0.2  # Circumference of the circle described by the cups in meters
SECONDS_PER_MINUTE = 60  # Number of seconds in a minute

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
    # Initialize Bluetooth
    uart = machine.UART(0, baudrate=9600)
    bt = bluetooth.BLE()
    bt.active(True)

    pulse_count = 0
    last_time = time.time()

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
            
            # Send data over Bluetooth
            uart.write(data)
            print("Data sent over Bluetooth")
            
            # Reset pulse count and timer
            pulse_count = 0
            last_time = time.time()
            
        time.sleep(0.1)  # Adjust sleep time as necessary to avoid high CPU usage

if __name__ == "__main__":
    main()



