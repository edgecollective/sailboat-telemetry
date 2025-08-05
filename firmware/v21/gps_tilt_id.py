import time
import struct
import board
import busio
import digitalio
import math

import adafruit_gps

from sx1262 import SX1262

SAILBOAT_ID = 1

uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)

gps = adafruit_gps.GPS(uart, debug=False)  # Use UART/pyserial

sx = SX1262(spi_bus=1, clk=3, mosi=3, miso=3, cs=3, irq=3, rst=3, gpio=3)

# LoRa
sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)
         
# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

gps.send_command(b"PMTK220,1000")

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
led.value=False

last_print = time.monotonic()



class SimpleMPU6050:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address
        
        # Wake up the device
        self._write_register(0x6B, 0x00)
        time.sleep(0.1)
        
        # Verify connection
        who_am_i = self._read_register(0x75)
        #if who_am_i not in [0x68, 0x71]:
         #   raise RuntimeError(f"Failed to find MPU6050, got WHO_AM_I: {hex(who_am_i)}")
    
    def _write_register(self, reg, value):
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.address, bytes([reg, value]))
        finally:
            self.i2c.unlock()
    
    def _read_register(self, reg):
        while not self.i2c.try_lock():
            pass
        try:
            result = bytearray(1)
            self.i2c.writeto_then_readfrom(self.address, bytes([reg]), result)
            return result[0]
        finally:
            self.i2c.unlock()
    
    def _read_registers(self, reg, count):
        while not self.i2c.try_lock():
            pass
        try:
            result = bytearray(count)
            self.i2c.writeto_then_readfrom(self.address, bytes([reg]), result)
            return result
        finally:
            self.i2c.unlock()
    
    @property
    def acceleration(self):
        # Read 6 bytes starting from ACCEL_XOUT_H (0x3B)
        data = self._read_registers(0x3B, 6)
        # Convert to signed 16-bit values
        x = struct.unpack('>h', data[0:2])[0] / 16384.0
        y = struct.unpack('>h', data[2:4])[0] / 16384.0
        z = struct.unpack('>h', data[4:6])[0] / 16384.0
        return (x, y, z)

def calculate_tilt_angle(z_accel):
    # Clamp z_accel to valid range for arccos
    z_clamped = max(-1.0, min(1.0, z_accel))
    # Calculate tilt angle: 0 degrees when z=1 (vertical), 180 degrees when z=-1
    tilt_radians = math.acos(z_clamped)
    tilt_degrees = tilt_radians * 180.0 / math.pi
    return tilt_degrees

# Usage
i2c = busio.I2C(board.SCL, board.SDA)
mpu = SimpleMPU6050(i2c)


while True:
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            continue
        #print(f"lat: {gps.latitude:.6f}, lon: {gps.longitude:.6f}")
        
        # Get accelerometer data and calculate tilt angle
        x, y, z = mpu.acceleration
        tilt = calculate_tilt_angle(z)
        
        
        print(f"Acceleration: {mpu.acceleration}")
        print(f"Tilt angle: {tilt:.2f} degrees")
        
        sendstring = f"{SAILBOAT_ID},{gps.latitude:.6f},{gps.longitude:.6f},{tilt:.2f}"
        print(sendstring)
        #sendstring=f"lat: {gps.latitude:.6f}, lon: {gps.longitude:.6f}"
        #sx.send(b'Hello World!')
        print ("sending...")
        sx.send(sendstring.encode())
        print("sent!")
        led.value=True
        time.sleep(.1)
        led.value=False
        time.sleep(.1)
        
        
        