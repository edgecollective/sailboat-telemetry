
import time

import board
import busio
import digitalio

import adafruit_gps

from sx1262 import SX1262

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
        print(f"lat: {gps.latitude:.6f}, lon: {gps.longitude:.6f}")
        
        sendstring=f"lat: {gps.latitude:.6f}, lon: {gps.longitude:.6f}"
        #sx.send(b'Hello World!')
        print ("sending...")
        sx.send(sendstring.encode())
        print("sent!")
        led.value=True
        time.sleep(.1)
        led.value=False
        time.sleep(.1)
        
        
        
