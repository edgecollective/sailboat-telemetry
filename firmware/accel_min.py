import board
import busio
import struct
import time

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

# Usage
i2c = busio.I2C(board.SCL, board.SDA)
mpu = SimpleMPU6050(i2c)
while True:

    print(f"Acceleration: {mpu.acceleration}")
    time.sleep(.1)

