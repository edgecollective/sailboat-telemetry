import board
import busio
import time

i2c = busio.I2C(board.SCL, board.SDA)
device_address = 0x68  # or your detected address

# Power management register
PWR_MGMT_1 = 0x6B

while not i2c.try_lock():
    pass

try:
    # Wake up the MPU-6050 (write 0 to power management register)
    i2c.writeto(device_address, bytes([PWR_MGMT_1, 0x00]))
    time.sleep(0.1)  # Give it time to wake up
finally:
    i2c.unlock()

# Now try the library
import adafruit_mpu6050
mpu = adafruit_mpu6050.MPU6050(i2c, address=device_address)
