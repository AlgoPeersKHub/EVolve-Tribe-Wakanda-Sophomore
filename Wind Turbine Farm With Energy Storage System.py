from machine import Pin, ADC, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import utime

# Initialize ADC for reading battery voltage
adc = ADC(Pin(26))
adc.width(ADC.WIDTH_12BIT)
adc.vref(3.3)

# Initialize I2C for LCD
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

def read_battery_voltage():
    # Read battery voltage and convert to percentage
    voltage = adc.read_u16() * 3.3 / 65535
    percentage = (voltage - 3.0) / (4.2 - 3.0) * 100
    return percentage

while True:
    # Read battery voltage and display on LCD
    battery_level = read_battery_voltage()
    lcd.putstr("Battery: {:.1f}%".format(battery_level))
    
    # Wait for a while before reading again
    utime.sleep(1)


