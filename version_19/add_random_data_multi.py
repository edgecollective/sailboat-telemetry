import time
import random
import csv
from datetime import datetime

# --- Configuration ---
NUM_SAILBOATS = 5
import os

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sailboat_data_multi.csv")
UPDATE_INTERVAL_SECONDS = 2

# --- Global Index Counter ---
global_index = 0

# --- Initial State ---
def create_sailboat_state(boat_id):
    """Creates the initial state for a single sailboat."""
    return {
        "id": f"Sailboat-{boat_id}",
        "lat": 41.77658 + (random.uniform(-0.01, 0.01)),
        "lon": -71.38852 + (random.uniform(-0.01, 0.01)),
        "compass": random.randint(0, 360),
        "tilt": random.uniform(-5, 5),
        "rssi": random.randint(-90, -30),  # RSSI in dBm, typical range for wireless signals
        "lat_lon_stepsize": 0.00005,
        "tilt_stepsize": 0.5,
        "compass_stepsize": 2,
        "rssi_stepsize": 3,  # RSSI can fluctuate by a few dBm
    }

def update_sailboat_data(state):
    """Updates a sailboat's state with new random data."""
    # Simulate some random movement and changes
    state["lat"] += random.uniform(-1, 1) * state["lat_lon_stepsize"]
    state["lon"] += random.uniform(-1, 1) * state["lat_lon_stepsize"]
    state["compass"] = (state["compass"] + random.uniform(-1, 1) * state["compass_stepsize"]) % 360
    
    # Make tilt return towards 0, but with random fluctuations
    state["tilt"] += random.uniform(-1, 1) * state["tilt_stepsize"]
    state["tilt"] *= 0.95 # Tendency to return to upright
    
    # Clamp tilt to a reasonable range
    state["tilt"] = max(-45, min(45, state["tilt"]))
    
    # Update RSSI with random fluctuations, generally weaker as distance increases
    state["rssi"] += random.uniform(-1, 1) * state["rssi_stepsize"]
    # Keep RSSI in realistic range (-100 to -20 dBm)
    state["rssi"] = max(-100, min(-20, state["rssi"]))
    
    return state

def main():
    """Main function to generate and write sailboat data."""
    
    sailboats = [create_sailboat_state(i + 1) for i in range(NUM_SAILBOATS)]
    
    # Write header to CSV file
    try:
        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["index", "timestamp", "sailboat_id", "latitude", "longitude", "compass_heading", "tilt", "rssi"])
        print(f"Initialized {OUTPUT_FILE} with header.")
    except IOError as e:
        print(f"Error initializing file: {e}")
        return

    print(f"Generating data for {NUM_SAILBOATS} sailboats every {UPDATE_INTERVAL_SECONDS} seconds...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            # Append new data line for each boat
            try:
                with open(OUTPUT_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    current_time = datetime.now().isoformat()
                    
                    for boat_state in sailboats:
                        global global_index
                        global_index += 1
                        boat_state = update_sailboat_data(boat_state)
                        
                        dataline = [
                            global_index,
                            current_time,
                            boat_state["id"],
                            f"{boat_state['lat']:.6f}",
                            f"{boat_state['lon']:.6f}",
                            f"{boat_state['compass']:.1f}",
                            f"{boat_state['tilt']:.2f}",
                            f"{boat_state['rssi']:.0f}"
                        ]
                        writer.writerow(dataline)
                        print(f"  - Wrote data for {boat_state['id']} (Index: {global_index}, RSSI: {boat_state['rssi']:.0f} dBm)")
            
            except IOError as e:
                print(f"Error writing to file: {e}")

            time.sleep(UPDATE_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("Stopping data generation.")

if __name__ == "__main__":
    main()