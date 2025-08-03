
import time
import random
import csv

# --- Configuration ---
NUM_SAILBOATS = 5
import os

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "sailboat_data_multi.csv")
UPDATE_INTERVAL_SECONDS = 2

# --- Initial State ---
def create_sailboat_state(boat_id):
    """Creates the initial state for a single sailboat."""
    return {
        "id": f"Sailboat-{boat_id}",
        "lat": 41.77658 + (random.uniform(-0.01, 0.01)),
        "lon": -71.38852 + (random.uniform(-0.01, 0.01)),
        "compass": random.randint(0, 360),
        "tilt": random.uniform(-5, 5),
        "lat_lon_stepsize": 0.00005,
        "tilt_stepsize": 0.5,
        "compass_stepsize": 2,
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
    
    return state

def main():
    """Main function to generate and write sailboat data."""
    
    sailboats = [create_sailboat_state(i + 1) for i in range(NUM_SAILBOATS)]
    
    # Write header to CSV file
    try:
        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["sailboat_id", "latitude", "longitude", "compass_heading", "tilt"])
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
                    for boat_state in sailboats:
                        boat_state = update_sailboat_data(boat_state)
                        
                        dataline = [
                            boat_state["id"],
                            f"{boat_state['lat']:.6f}",
                            f"{boat_state['lon']:.6f}",
                            f"{boat_state['compass']:.1f}",
                            f"{boat_state['tilt']:.2f}"
                        ]
                        writer.writerow(dataline)
                        print(f"  - Wrote data for {boat_state['id']}")
            
            except IOError as e:
                print(f"Error writing to file: {e}")

            time.sleep(UPDATE_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("Stopping data generation.")

if __name__ == "__main__":
    main()
