import time
import board
from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15

# Initialize I2C
i2c = board.I2C()

# Initialize ADC
ads = ADS1015(i2c)

# Select channel A0
channel = AnalogIn(ads, ads1x15.Pin.A0)

VCC = 5.26
WATER_DENSITY = 1000
ACCELERATION = 9.80655
PRESSURE = 0.0
DEPTH = 0.0

# Continuously read voltage
while True:
    try: 
        print(f"Voltage: \t{channel.voltage:.3f} V")
        
        PRESSURE = (channel.voltage-(VCC*0.1)) / (VCC*0.75)
        if(PRESSURE < 0.0):
            PRESSURE = 0.0
        print(f"Pressure: \t{PRESSURE:.2f} Mpa")

        DEPTH = (PRESSURE*1000000)/(WATER_DENSITY/ACCELERATION)
        print(f"Depth: \t\t{DEPTH:.2f} m\n")
    except:
        print("Error Reading Pressure Sensor")
    time.sleep(0.5)
