import machine
import utime

# Define GPIO pins
MOTOR_PIN = machine.Pin(0, machine.Pin.OUT)  # Motor control pin (PWM)
POTENTIOMETER_PIN = machine.ADC(26)           # Potentiometer analog input pin

# Define motor PWM object
motor_pwm = machine.PWM(MOTOR_PIN)

def read_potentiometer_voltage():
    """
    Read voltage from potentiometer and map it to motor speed range.
    """
    # Read analog voltage from potentiometer (0-65535)
    potentiometer_value = POTENTIOMETER_PIN.read_u16()

    # Map potentiometer value to motor speed range (0-1023)
    motor_speed = int((potentiometer_value / 65535) * 1023)
    
    return motor_speed

def control_motor_speed(speed):
    """
    Control motor speed using PWM.
    """
    # Set motor PWM duty cycle based on speed
    motor_pwm.duty_u16(speed)

# Main loop
while True:
    # Read potentiometer voltage and control motor speed
    speed = read_potentiometer_voltage()
    control_motor_speed(speed)

    # Delay for stability
    utime.sleep(0.1)
