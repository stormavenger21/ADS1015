import time
import board
import io
import sys
from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15




def main():
    # Initialize I2C
    i2c = board.I2C()
    
    # Initialize ADC
    ads = ADS1015(i2c)
    
    # Select channel A0
    channel0 = AnalogIn(ads, ads1x15.Pin.A0)
    while True:
        try:
            print(f"Voltage: \t{channel0.voltage:.3f} V")
        except:
            print("error reading voltage")
        time.sleep(0.05)
    #depth(channel0)

def depth(ADC_ch):
    VCC = 5.26
    WATER_DENSITY = 1000
    ACCELERATION = 9.80655
    PRESSURE = 0.0
    DEPTH = 0.0
    try: 
        print(f"Voltage: \t{ADC_ch.voltage:.3f} V")
        
        PRESSURE = (ADC_ch.voltage-(VCC*0.1)) / (VCC*0.75)
        if(PRESSURE < 0.0):
            PRESSURE = 0.0
        print(f"Pressure: \t{PRESSURE:.2f} Mpa")

        DEPTH = (PRESSURE*1000000)/(WATER_DENSITY/ACCELERATION)
        print(f"Depth: \t\t{DEPTH:.2f} m\n")
    except:
        print("Error Reading Pressure Sensor")


if __name__=="__main__":
    main()
