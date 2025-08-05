import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

# The WHO_AM_I register should return 0x68
WHO_AM_I_REG = 0x75
device_address = 0x68  # or 0x69 if that's what your scan showed

while not i2c.try_lock():
    pass

try:
    result = bytearray(1)
    i2c.writeto_then_readfrom(device_address, bytes([WHO_AM_I_REG]), result)
    print(f"WHO_AM_I register value: {hex(result[0])}")
finally:
    i2c.unlock()
