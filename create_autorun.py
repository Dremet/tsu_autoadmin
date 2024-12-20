import os
import sys
import time
import random


### CONSTANTS ###

NUMBER_TRACKS = 3

TRACKS = [
    "Barcelona GP - Catalunya v1.06",
    "Silverstone Circuit V1.04",
    "Circuit of the Americas v1.031",
    "Sepang Circuit V2.01",
    "Hockenheimring GP v1.41",
    "Motorsport Arena Oschersleben v1",
    "National Racetrack Monza v1.5"
]

VEHICLES = [
    "Ferrari 488 GTE NWT",
    "V8Vantage AMRGTE NWT",
    "Porsche911 RSR-19NWT",
    "BMW M8 GTE NWT",
    "Ford GT LM GTE NWT"
]


### HELPER FUNCTIONS ###

def run_function_by_name(function_name):
    """Run a function in this file by its name."""
    if function_name in globals() and callable(globals()[function_name]):
        globals()[function_name]()
    else:
        print(f"Error: Function '{function_name}' not found or is not callable.")


def wait_for_autorun_file(func):
    """Decorator to wait until 'autorun.src' file disappears before running the function."""
    def wrapper(*args, **kwargs):
        while os.path.exists("autorun.src"):
            print("Waiting for 'autorun.src' to be removed...")
            time.sleep(0.5)
        return func(*args, **kwargs)
    return wrapper


def write_to_autorun(commands):
    """
    Helper function to write commands to 'autorun.src' file.
    Overwrites the file if it exists.
    """
    with open("autorun.src", "w") as file:
        file.write("\n".join(commands) + "\n")


def select_random_elements(my_list, n=3):
    """Select `n` random elements from the list."""
    if n > len(my_list):
        raise ValueError("n cannot be greater than the length of the list.")
    return random.sample(my_list, n)

def save_quali_marker_file():
    """
    Creates an empty file called 'next_event_is_quali'.
    Used to allow the other python scripts to know at which state of the session we are.
    """
    with open("next_event_is_quali", "w") as file:
        pass

### FUNCTIONS TO RUN AT CERTAIN TIMES ###

@wait_for_autorun_file
def announce_1_minute():
    commands = [
        "/broadcast Session starts in 1 minute!",
    ]
    write_to_autorun(commands)

@wait_for_autorun_file
def skip_to_new_session():
    commands = [
        "/continue",
    ]
    write_to_autorun(commands)

@wait_for_autorun_file
def start_session():
    save_quali_marker_file()

    commands = [
        "/timerOn = True",
        "/broadcast Session started! Setting things up…",
        "/admins /clear",
        "/admins /add 76561197989276622", # dremet
        "/admins /add 76561198131829686", # mcvizn
        "/admins /add 76561198096169747", # cyberpunk
        "/vehicles /clear",
        "/levels /clear",
        # turn off fuel selection at beginning of race
    ]

    # add vehicles
    commands+=[f"/vehicle /add '{vehicle}'" for vehicle in VEHICLES]

    # add randomly selected tracks
    tracks = select_random_elements(TRACKS, NUMBER_TRACKS)

    # first track twice because we hotlap on it
    first_track = tracks[0]
    tracks.insert(0, first_track)

    commands+=[f"/level /add '{track}'" for track in tracks]

    print(commands)

    commands+=[ 
        "/broadcast ### Success! Everything has been set up! Enjoy the races!",
        "/broadcast # There is a 1 lap quali on the first track. Starting order is always 'Last Event'.",
        "/broadcast # Fuel consumption and tire degradation are randomized for each race."
    ]

    write_to_autorun(commands)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_autorun.py <function_name>")
    else:
        function_name = sys.argv[1]
        run_function_by_name(function_name)
