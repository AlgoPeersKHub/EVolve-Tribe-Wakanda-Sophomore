from machine import ADC, Pin
import utime

# Initialize the ADC pin
adc = ADC(Pin(26))  # GP26 corresponds to ADC0

def anemometer_reading():
    # Read the ADC value
    adc_value = adc.read_u16()
    # Convert the ADC value to voltage (3.3V reference, 16-bit resolution)
    voltage = adc_value * 3.3 / 65535
    return voltage

while True:
    voltage = anemometer_reading()
    # Print the voltage (which corresponds to wind speed)
    print("Wind speed voltage:", voltage)
    utime.sleep(1)
