#Importing all the necassary modules

from machine import Pin, I2C        
from time import sleep
import bme280       #See the coding section of the instructions on how to import this module. 

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)    #initializing the I2C method 
bme = bme280.BME280(i2c=i2c)       #BME280 object created

while True: #Creates a while loop which reads the values from the BME
  print(bme.values) #Prints the BME values to "shell"
  sleep(10)           #Detects BME values every 10 seconds. You can change this, by changing the number 10 to any number you like.


temp_adc = machine.ADC(4) #ADC pin 4 is an Analog to Digital Pin that has a temperature sensor.
while True:
    ADC_read = temp_adc.read_u16()  #Here we are reading the digital values across ADC pin 4. These digital values change depending on the temperature. 
    ADC_voltage = (ADC_read* (3.3 / (4095)) #Here we are converting the digital values into voltage values. 
                                             #The voltage values the ADC can take swing from 0V to 3.3V, so if we divide them by the number of digital bits, it gives the voltage per bit. 
                                             #Multiplying by the digital value gives the voltage across ADC 4. 
    temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721 # This equations simply converts the voltage values into temperature values in degreees.
    print("Temperature: {}°C".format(temperature_celcius)) # Here we simply print the temperature values. 
    time.sleep_ms(500) # The temperature is being read every 500miliseconds, we can change this to how ever miliseconds we want.



rain_adc = machine.ADC(26) #Set the raindrop sensor ADC to 26
conversion_factor = 100 / (4095) #Converts the digital values to a percentage as shown in the temperature sensor. The percentage is the percentage of area of the sensor that is NOT covered by rain.

while True:
    rainCoverage = 100 - (rain_adc.read_u16() * conversion_factor) #Reads the digital value from the rain_ADC and then subtracts it from 100 to get the percentage of area of the sensor that is covered by rain.
    print(round(rainCoverage, 1), "%") #printing rain coverage values. The "round(rainCoverage, 1)" part rounds the values of "rainCoverage" to 1d.p.
    utime.sleep_ms(1000) #The rain is being read every 1000miliseconds, we can change this to how ever miliseconds we want.

