#import all the necessary librabries for the project.
import machine #This library helps control the electronic parts connected to the raspbery pi, like the sensors.

import time #This library helps with tasks related to time, like  measuring how long something takes, or keeping track of the current time.

import bluetooth #This library helps devices talk to each other wirelessly, like sending messages to your App on Mit App Inventor.


# Define pins for the Hall effect sensor and wind vane potentiometer

hall_pin = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP) #This line sets up a pin (like an electronic connection) on the raspberry pi pico. 
                                                                #It's connected to a Hall effect sensor, which detects magnetic fields. 
                                                                #The sensor is set up to read whether there's a magnetic field present (IN), and 
                                                                #it's also set up with a pull-up resistor (PULL_UP), which helps stabilize the signal.



potentiometer_pin = machine.Pin(15, machine.Pin.IN) #This line sets up another wire on the raspberry pi pico. 
                                                    #It's like setting up a wire to check if something is on or off, like a switch.


# variables
circumference = 0.2  #This line means that the distance around a circle, like the path the anemometer cups follow, is 0.2 units long. 
                     #In this case, it's measured in meters. 
                     #Note: you need to adjust this number according to your set up.

seconds_per_min = 60  # Number of seconds in a minute


def calculate_wind_speed(pulse_count, time_interval): #This line defines a function named calculate_wind_speed that takes two inputs: 
                                                      #pulse_count (the number of rotations of the anemometer cups) and 
                                                      #time_interval (the time elapsed during those rotations).
    
    rotations_per_second = pulse_count / time_interval #This line calculates how many times the anemometer cups rotate per second. 
                                                       #It divides the total number of rotations (pulse_count) by the time it took to make those rotations (time_interval).

    wind_speed_mps = rotations_per_second * circumference #This line calculates the wind speed in meters per second (mps). 
                                                        #It multiplies the number of rotations per second (rotations_per_second) by the circumference of the circle described by the anemometer cups.
    
    return wind_speed_mps #This line returns the calculated wind speed in meters per second as the output of the function, 
                           #so it can be used elsewhere in the program.



def read_wind_direction(potentiometer_pin): #This line defines a function named read_wind_direction that takes one input parameter: potentiometer_pin. 
                                            #This parameter represents the pin connected to a potentiometer used to measure wind direction.

    analog_value = potentiometer_pin.read_u16()  #This line reads the analog value from the potentiometer pin. 
                                                 #The read_u16() function reads the voltage level at the pin and converts it into a 16-bit unsigned integer value. 
                                                 #This value represents the position of the potentiometer's wiper.
    
    wind_direction_degrees = analog_value * 360 / 65535  #This line calculates the wind direction in degrees based on the analog value read from the potentiometer. 
                                                         #It converts the analog value to a range from 0 to 360 degrees, 
                                                         #assuming the potentiometer covers the full range of motion from 0 to 65535 (the maximum value for a 16-bit unsigned integer).

    return wind_direction_degrees #This line returns the calculated wind direction in degrees as the output of the function, so it can be used elsewhere in the program.



def main(): #This line defines a function named main().
    
    uart = machine.UART(0, baudrate=9600) #This line initializes the UART (Universal Asynchronous Receiver-Transmitter) communication interface. 
                                          #UART is used for serial communication, and here it's set up with UART port 0 and a baud rate of 9600 bits per second.

    bt = bluetooth.BLE() #This line initializes Bluetooth Low Energy (BLE) communication. It sets up the Bluetooth interface.
    bt.active(True) #This line activates the Bluetooth interface, making it ready to send and receive data.


    pulse_count = 0 #This line initializes a variable pulse_count to keep track of the number of pulses detected by the Hall effect sensor (anemometer cups rotation count).
    last_time = time.time() #This line records the current time using the time.time() function and assigns it to the variable last_time. It's used for timing calculations.


    while True: #This line starts forever loop, meaning the code inside the loop will keep running forever.

        hall_state = hall_pin.value() #This line reads the current state (0 or 1) of the Hall effect sensor pin and assigns it to the variable hall_state.
        
        
        if hall_state == 0:  #This line checks if the state of the Hall effect sensor is 0, indicating a pulse (rotation of the anemometer cups). 
                             #If true, it executes the following block of code.

            pulse_count += 1 #This line increments the pulse_count variable, counting the number of pulses detected.
        

        current_time = time.time() #This line records the current time again and assigns it to the variable current_time.
        time_interval = current_time - last_time #This line calculates the time interval since the last measurement by subtracting last_time from current_time.
        

        last_time = current_time #This line updates last_time to the current time, preparing for the next interval measurement.

        
        # Calculate wind speed every minute
        if time_interval >= SECONDS_PER_MINUTE: #This line checks if the time interval has reached or exceeded one minute.
            
            wind_speed = calculate_wind_speed(pulse_count, time_interval) #This line calculates the wind speed using the calculate_wind_speed() function, 
                                                                          #passing the pulse count and time interval as arguments
            
            wind_direction = read_wind_direction(position_pin) #This line calculates the wind direction using the read_wind_direction() function, 
                                                               #passing the position pin as an argument.

            data = "Wind Speed: {:.2f} m/s\nWind Direction: {:.2f} degrees\n".format(wind_speed, wind_direction) #This line formats the wind speed and wind direction values into a string named data, 
                                                                                                                 #with two decimal places for precision.
            
            # Send data over Bluetooth
            uart.write(data) #This line sends the formatted data over Bluetooth using the UART interface
            print("Data sent over Bluetooth") #This line prints a message to the console indicating that the data has been sent over Bluetooth.

            
            # Reset pulse count and timer
            pulse_count = 0 #This line resets the pulse count variable for the next minute.

            last_time = time.time() #This line resets the last time variable for the next interval measurement.

            
        time.sleep(0.1)  # This line adds a short delay of 0.1 seconds to avoid high CPU usage and allow other tasks to run smoothly.
        
if __name__ == "__main__": #This line checks if the script is being run directly (not imported as a module).
    main() #This line calls the main() function to start executing the code.



