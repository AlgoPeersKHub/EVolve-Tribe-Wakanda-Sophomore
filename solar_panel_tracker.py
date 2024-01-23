#Import the necassary modules for the Raspberry Pi Pico
import machine
import utime
from servo import Servo

solar_servo = Servo(pin_id=17) #set the sevo pin to pin 17

#In this example we are using 3 LDRs.
ldr_1 = machine.ADC(28) # Here we tell the Raspberry Pi pico which pins the LDRs are on
ldr_2 = machine.ADC(27) # Note that the LDRs are all on ADC pins.
ldr_3 = machine.ADC(26) # This means the analog signals from the LDR get converted to digital signals which are read by the Pi.
 
while True: 
    reading1 = int(ldr_1.read_u16()) #These commands make the Raspberry Pi read the digital signals and turn them into integers
    reading2 = int(ldr_2.read_u16())
    reading3 = int(ldr_3.read_u16())

    #Because the voltage across an LDR decreases as you increase the light intensity, the LDR with the lowest value shoudl be the one the sevo turns towards
    variables = {'reading1': reading1, 'reading2': reading2, 'reading3': reading3}
    smallest_variable = min(variables, key=variables.get)

    #Here we are telling the Raspberry Pi how much we need to move the servo based on which LDR is recieving the highest light intensity.
    if smallest_variable == "reading3": #If the smallest reading is ldr_3 then it will move the servo to an angle of 150 degrees.
        my_servo.write(150)    
    elif smallest_variable == "reading2": #If the smallest reading is ldr_2 then it will move the servo to an angle of 90 degrees.
        my_servo.write(90)
    else:                                
        my_servo.write(30) #If the smallest reading is ldr_1 then it will move the servo to an angle of 30 degrees
    #Feel free to adjust the angles to suit your design
  
    #Prints all the values of the LDRs and the maximum value
    print("ldr_1: ",reading1)
    print("ldr_2: ",reading2)
    print("ldr_3: ",reading3)
    print("max_val: ", smallest_variable)
    utime.sleep(0.5) #This line tells the Raspberry Pi how often it should check the LDRs. In this example, we have set it to "0.5" so here the Raspberry Pi is checking the LDR every 0.5 seconds.
