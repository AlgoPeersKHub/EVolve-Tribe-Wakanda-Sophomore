from machine import ADC, Pin, UART
import utime

# Initialize the ADC pin
adc = ADC(Pin(26))  # GP26 corresponds to ADC0

# Initialize UART for Bluetooth communication
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

def read_anemometer():
    # Read the ADC value
    adc_value = adc.read_u16()
    # Convert the ADC value to voltage (3.3V reference, 16-bit resolution)
    voltage = adc_value * 3.3 / 65535
    return voltage

while True:
    voltage = read_anemometer()
    # Print the voltage (which corresponds to wind speed)
    print("Wind speed voltage:", voltage)
    # Send the voltage via Bluetooth
    uart.write(f"{voltage}\n")
    utime.sleep(1)
