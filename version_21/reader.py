import serial
import time

# Serial port configuration
# Adjust these settings to match your setup
SERIAL_PORT = '/dev/ttyACM0'  # Change to your serial port (Windows: 'COM3', etc.)
BAUD_RATE = 115200  # Adjust to match your device's baud rate
LOG_FILE = 'log.txt'

def main():
    try:
        # Open serial connection
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
        print(f"Logging data to {LOG_FILE}")
        print("Press Ctrl+C to stop")
        
        # Open log file in append mode (creates if doesn't exist)
        with open(LOG_FILE, 'a') as log_file:
            while True:
                try:
                    # Read line from serial port
                    line = ser.readline().decode('utf-8').strip()
                    
                    if line:  # Only process non-empty lines
                        # Print what we received from serial port
                        print(f"Received from serial: {line}")
                        
                        # Check if line matches expected format: sailboat_id,lat,lon,tilt
                        parts = line.split(',')
                        if len(parts) == 4:
                            try:
                                # Validate format: sailboat_id (str), lat (float), lon (float), tilt (float)
                                sailboat_id = str(parts[0])  # sailboat_id
                                lat = float(parts[1])  # lat
                                lon = float(parts[2])  # lon
                                tilt = float(parts[3])  # tilt
                                
                                # Add reader timestamp as first column
                                reader_timestamp = int(time.time() * 1000)  # Unix timestamp in milliseconds
                                log_entry = f"{reader_timestamp},{sailboat_id},{lat},{lon},{tilt}\n"
                                
                                # Write to file and flush immediately
                                log_file.write(log_entry)
                                log_file.flush()
                                
                                # Print what we wrote to log file
                                print(f"Logged: {log_entry.strip()}")
                                
                            except ValueError:
                                print(f"Invalid format - skipping: {line}")
                        else:
                            print(f"Wrong number of fields ({len(parts)}) - skipping: {line}")
                        
                except UnicodeDecodeError:
                    # Skip lines that can't be decoded
                    pass
                    
    except serial.SerialException as e:
        print(f"Error opening serial port {SERIAL_PORT}: {e}")
        print("Please check:")
        print("1. The serial port name is correct")
        print("2. The device is connected")
        print("3. You have permission to access the port")
        
    except KeyboardInterrupt:
        print("\nStopping data logging...")
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        
    finally:
        try:
            ser.close()
            print("Serial connection closed")
        except:
            pass

if __name__ == "__main__":
    main()
