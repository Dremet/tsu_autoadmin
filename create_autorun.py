import os
import sys
import time
import random


### CONSTANTS ###

NUMBER_TRACKS = 3

TRACKS = [
    ("Circuit of the Americas v1.031", 1),
    ("Sepang Circuit V2.02", 1),
    ("Barcelona GP - Catalunya v1.06", 1),
    ("Silverstone Circuit V1.05", 1),
    ("Japanese GP v2.04", 1),
    ("Balaton Park Circuit v1.01", 1),
    ("Hockenheimring GP v1.42", 1),
    ("Motorsport Arena Oschersleben v1", 1),
    ("National Racetrack Monza v1.5", 1),
    ("Nanoli Full Circuit v1.4", 1),
    ("TT Circuit Assen V1.7", 1),
    ("Elethasia Island Circuit v1.01", 1),
    ("Watkins Glen International v1.3", 1),
    ("Spa Francorchamps GP v3.12", 1),
    ("Hungaroring V2.04", 1),
    ("Canadian GP v1.12", 1),
    ("Australian GP v1.16", 1),
    ("Daytona Road Course V2.01", 1),
]

VEHICLES = [
    "Ferrari 488 GTE NWT",
    "V8Vantage AMRGTE NWT",
    "Porsche911 RSR-19NWT",
    "BMW M8 GTE NWT",
    "Ford GT LM GTE NWT",
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


def select_random_elements_with_weights(tracks_with_weights, n=3):
    """
    Select `n` random elements from a list of (element, weight) tuples with weighted probabilities.
    Elements with lower weights are less likely to be selected.
    """
    if n > len(tracks_with_weights):
        raise ValueError("n cannot be greater than the length of the list.")

    # Split the list of tuples into separate lists for items and weights
    items, weights = zip(*tracks_with_weights)

    # Use random.choices with weights to bias selection
    selected = random.choices(items, weights=weights, k=n)

    # Ensure unique selections (if duplicates occur, reselect)
    while len(set(selected)) < n:
        selected = random.choices(items, weights=weights, k=n)

    return selected


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
        "/admins /add 76561197989276622",  # dremet
        "/admins /add 76561198131829686",  # mcvizn
        "/admins /add 76561198096169747",  # cyberpunk
        "/vehicles /clear",
        "/levels /clear",
        # turn off fuel selection at beginning of race
    ]

    # add vehicles
    commands += [f"/vehicle /add '{vehicle}'" for vehicle in VEHICLES]

    # add randomly selected tracks
    tracks = select_random_elements_with_weights(TRACKS, NUMBER_TRACKS)

    # duplicate each track for qualification
    duplicated_tracks = []
    for track in tracks:
        # Add the track twice (first for hotlapping, then for race)
        duplicated_tracks.append(track)  # Hotlapping
        duplicated_tracks.append(track)  # Race

    commands += [f"/level /add '{track}'" for track in duplicated_tracks]

    print(commands)

    commands += [
        "/broadcast ### Success! Everything has been set up! Enjoy the races!",
        "/broadcast # There is a 1 lap qualifier for each track. Starting order is always 'Last Event'.",
        "/broadcast # Fuel consumption and tire degradation are randomized for each race.",
    ]

    write_to_autorun(commands)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(select_random_elements_with_weights(TRACKS, NUMBER_TRACKS))
        print("Usage: python create_autorun.py <function_name>")
    else:
        function_name = sys.argv[1]
        run_function_by_name(function_name)
