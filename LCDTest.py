
from pico_i2c_lcd import I2cLcd
from machine import I2C
from machine import Pin
import utime as time

i2c = I2C(id=0,scl=Pin(1),sda=Pin(0),freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16) # LCD 16x2

lcd.putstr('Hello Algo Peer!')
lcd.putstr('Code Solve  Loop')

led = Pin(5, Pin.OUT)  # Configure pin 5 as an output

# Turn on the LED
led.value(1)

# Wait for a few seconds
time.sleep(5)

# Turn off the LED
led.value(0)