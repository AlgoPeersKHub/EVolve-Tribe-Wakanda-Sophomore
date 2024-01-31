import utime

from machine import I2C, Pin

dev = I2C(1, freq = 400000, scl=Pin(15), sda=Pin(14))
devices = dev.scan()

for device in devices:
    print(device)

address = 72

def readConfig():
    dev.writeto(address, bytearray([1]))
    result = dev.readfrom(address,2)
    return result[0]<<8 | result[1]

def readValue():
    dev.writeto(address, bytearray([0]))
    result = dev.readfrom(address,2)

    config = readConfig()
    config &= ~(7<<12) & ~(7<<9)
    config |= (4<<12) | (1<<9) | (1<<15)
    
    config = [ int(config>>i & 0xff) for i in (8,0)]

    dev.writeto(address, bytearray([1] + config))

    return result[0]<<8 | result[1]

print(bin(readConfig()))

whileTrue:
    val = readValue()
    print((3.3/26250) * val)
    utime.sleep(0.1)

#from https://www.youtube.com/watch?v=HiuNYLDvY9k&t=334s
