import machine # This line imports the machine module. The machine module provides functions 
               # related to hardware control, such as controlling GPIO pins, SPI, I2C, UART, etc.

import utime   #This line imports the utime module. The utime module in MicroPython provides functions 
               #for working with time-related operations.


# Define GPIO pins
MOTOR_PIN = machine.Pin(0, machine.Pin.OUT)  """This line initializes a variable named MOTOR_PIN.
                                             machine.Pin(0, machine.Pin.OUT) creates a Pin object for pin 0 on the microcontroller, 
                                             indicating that it will be used for output.
                                             This line suggests that pin 0 is designated to control a motor, as it's set as an output pin. 
                                             The actual control of the motor would happen by sending signals to this pin."""

POTENTIOMETER_PIN = machine.ADC(26)    """This line initializes a variable named POTENTIOMETER_PIN.
                                          machine.ADC(26) creates an ADC (Analog-to-Digital Converter) object on pin 26 of the microcontroller.
                                          This line suggests that pin 26 is connected to a potentiometer, which is a variable resistor used to generate analog signals. 
                                          The ADC is used to read the analog voltage from the potentiometer, allowing the microcontroller to determine the position or 
                                          level set by the potentiometer."""

# Define motor PWM object
motor_pwm = machine.PWM(MOTOR_PIN)     """This part creates a Pulse Width Modulation (PWM) object using the PWM class from the machine module. 
                                          PWM is a method used to generate analog-like signals (varying voltage levels) using digital signals (high and low voltage levels). 
                                          In MicroPython, PWM objects are used to control the intensity of a digital signal on a specific pin, allowing for precise control 
                                          over devices such as motors or LEDs."""

def read_potentiometer_voltage():      """This line defines a function named read_potentiometer_voltage(). 
                                          Functions in Python are defined using the def keyword followed by the function name and parentheses containing any parameters. 
                                          In this case, the function doesn't take any parameters."""
    
    # Read analog voltage from potentiometer (0-65535)
    potentiometer_value = POTENTIOMETER_PIN.read_u16() """This line reads the analog voltage from the potentiometer connected to the POTENTIOMETER_PIN."""

    # Map potentiometer value to motor speed range (0-1023)
    motor_speed = int((potentiometer_value / 65535) * 1023) """This line maps the potentiometer value read to a motor speed range of 0-1023.
                                                               (potentiometer_value / 65535) normalizes the potentiometer value to a range between 0 and 1."""
    
    return motor_speed                                         """This line returns the calculated motor speed value to the caller of the function when it's called. 
                                                                  It ends the function execution and passes the value of motor_speed back to the code that 
                                                                  called read_potentiometer_voltage().""" 


def control_motor_speed(speed):      """This line defines a function named control_motor_speed that takes one parameter speed."""

    # Set motor PWM duty cycle based on speed
    motor_pwm.duty_u16(speed)  """This line sets the duty cycle of the PWM signal generated by the motor_pwm object."""



# Main loop
while True:   """This creates an infinite loop, which is a common pattern for programs that continuously perform some action, 
                  like reading sensors or controlling hardware."""
    
    # Read potentiometer voltage and control motor speed
    speed = read_potentiometer_voltage()  """This line calls the read_potentiometer_voltage() function to read the voltage from the potentiometer and assigns the result to the variable speed. 
                                             This value represents the desired speed for the motor."""

    control_motor_speed(speed)  """This line calls the control_motor_speed() function with the speed variable as an argument. 
                                   This function sets the motor speed based on the value of speed."""

    # Delay for stability
    utime.sleep(0.1) """This line causes the program to pause execution for 0.1 seconds. """