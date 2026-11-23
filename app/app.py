import time
import board
from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15

# Initialize I2C
i2c = board.I2C()

# Initialize ADC
ads = ADS1015(i2c)

# Select channel A0
channel = AnalogIn(ads, ads1x15.Pin.A0)

# Continuously read voltage
while True:
    print(f"Voltage: {channel.voltage:.3f} V")
    time.sleep(0.5)
