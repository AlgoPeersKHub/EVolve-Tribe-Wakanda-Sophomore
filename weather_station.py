
from machine import Pin, I2C  
import bluetooth  
from time import sleep
import machine
import utime
import bme280       

#setting up sensors
i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)    #initializing the I2C method 
temp_adc = machine.ADC(4) #ADC pin 4 is an Analog to Digital Pin that has a temperature sensor.
rain_adc = machine.ADC(26) #Set the raindrop sensor ADC to 26
ldr_adc = machine.ADC(27)
# Set up UART communication with HC-05 Bluetooth module
uart = machine.UART(0, baudrate=9600)
bluetooth.atcmd("AT+ROLE=0")  # Set HC-05 as slave


while True:
    
    #collect pressure data from BME280
    current_time = int(utime.time())
    bme = bme280.BME280(i2c=i2c)       

    #collect temperature data from onboard temp sensor
    ADC_read_temperature = temp_adc.read_u16()  #Here we are reading the digital values across ADC pin 4. These digital values change depending on the temperature. 
    ADC_voltage_temperature = (ADC_read_temperature* (3.3 / 4095)) #Here we are converting the digital values into voltage values. The voltage values the ADC can take swing from 0V to 3.3V, so if we divide them by the number of digital bits, it gives the voltage per bit. 
    temperature_celcius = 27 - (ADC_voltage_temperature - 0.706)/0.001721 # This equations simply converts the voltage values into temperature values in degreees.

    #collect rain coverage values
    rain_coverage = 100 - (rain_adc.read_u16() * (100 / (4095))) #Reads the digital value from the rain_ADC and then subtracts it from 100 to get the percentage of area of the sensor that is covered by rain.

    #collect ldr values
    ADC_read_ldr = ldr_adc.read_u16()
    ADC_voltage_ldr = (ADC_read_ldr * (3.3/4095))#convert from 
    ldr_lux = ADC_voltage_ldr #somehow convert the values form voltages to lux values
    
    data = str(temperature_celcius,"," , bme.values,",", rain_coverage, ",", ldr_lux).encode()

    uart.write(data)

    # Optional: Wait for a brief moment before sending the next data
    utime.sleep_ms(1000)
