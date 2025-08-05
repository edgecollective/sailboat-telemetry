from sx1262 import SX1262
import time
import board
import digitalio
import random

sx = SX1262(spi_bus=1, clk=3, mosi=3, miso=3, cs=3, irq=3, rst=3, gpio=3)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# LoRa
sx.begin(freq=923, bw=500.0, sf=12, cr=8, syncWord=0x12,
         power=-5, currentLimit=60.0, preambleLength=8,
         implicit=False, implicitLen=0xFF,
         crcOn=True, txIq=False, rxIq=False,
         tcxoVoltage=1.7, useRegulatorLDO=False, blocking=True)

# FSK
##sx.beginFSK(freq=923, br=48.0, freqDev=50.0, rxBw=156.2, power=-5, currentLimit=60.0,
##            preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
##            addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
##            crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
##            fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
##            tcxoVoltage=1.6, useRegulatorLDO=False,
##            blocking=True)

# Base coordinates for Edgewood area (approximate)
base_lat = 42.3601
base_lon = -71.0589

while True:
    # Generate fake GPS data with small random variations
    lat = base_lat + (random.random() - 0.5) * 0.01  # ±0.005 degrees variation
    lon = base_lon + (random.random() - 0.5) * 0.01  # ±0.005 degrees variation
    
    # Generate fake tilt data (0-360 degrees)
    tilt = random.random() * 360
    
    # Create comma-separated string
    data_string = f"{lat:.6f},{lon:.6f},{tilt:.2f}"
    
    sx.send(data_string.encode())
    print(f"sent: {data_string}")
    
    led.value = True
    time.sleep(0.1)
    led.value = False

    time.sleep(3)