import machine
import utime
import matplotlib.pyplot as plt

# Configure ADC
adc = machine.ADC(0)  # ADC pin 0 (GP26 on Raspberry Pi Pico)

# Variables for plotting
times = []
voltages = []

# Main loop
try:
    while True:
        # Read ADC value and convert to voltage
        adc_value = adc.read_u16()
        voltage = (adc_value / 65535) * 3.3  # Convert ADC value to voltage

        # Store time and voltage for plotting
        times.append(utime.ticks_ms())
        voltages.append(voltage)

        # Print voltage and sleep for a while
        print("Voltage: {:.2f}V".format(voltage))
        utime.sleep(1)

except KeyboardInterrupt:
    # Plot the data when Ctrl+C is pressed
    plt.plot(times, voltages)
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (V)')
    plt.title('LiPo Battery Voltage Monitoring')
    plt.grid(True)
    plt.show()
