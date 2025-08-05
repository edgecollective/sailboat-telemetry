from sx1262 import SX1262
import time
import board
import digitalio

sx = SX1262(spi_bus=1, clk=10, mosi=11, miso=12, cs=3, irq=20, rst=15, gpio=2)

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

while True:
    print("listening...")
    msg, err = sx.recv()
    if len(msg) > 0:
        error = SX1262.STATUS[err]
        print(f"Raw message: {msg}")
        print(f"Status: {error}")
        
        # Try to get RSSI information (try common method names)
        try:
            if hasattr(sx, 'getRSSI'):
                rssi = sx.getRSSI()
                print(f"RSSI: {rssi} dBm")
            elif hasattr(sx, 'rssi'):
                rssi = sx.rssi()
                print(f"RSSI: {rssi} dBm")
            elif hasattr(sx, 'lastRSSI'):
                rssi = sx.lastRSSI()
                print(f"RSSI: {rssi} dBm")
            elif hasattr(sx, 'getLastRSSI'):
                rssi = sx.getLastRSSI()
                print(f"RSSI: {rssi} dBm")
            else:
                print("RSSI: Not available (method not found)")
        except Exception as e:
            print(f"RSSI: Error getting RSSI - {e}")
        
        # Parse comma-separated data
        try:
            data_string = msg.decode('utf-8')
            parts = data_string.split(',')
            
            if len(parts) == 3:
                lat = float(parts[0])
                lon = float(parts[1])
                tilt = float(parts[2])
                
                print(f"Latitude: {lat}")
                print(f"Longitude: {lon}")
                print(f"Tilt: {tilt} degrees")
            else:
                print("Invalid data format - expected 3 comma-separated values")
                
        except Exception as e:
            print(f"Error parsing data: {e}")
        
        led.value = True
        time.sleep(0.1)
        led.value = False
        
        print("---")