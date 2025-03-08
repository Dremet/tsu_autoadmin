import os
import random

### SETUP
# QUALI
QUALI_LAPS = 1
QUALI_MAX_MINUTES = 3
# QUALI_FUEL = 500
# QUALI_TIRES = 800

# RACE
race_laps = random.randint(8, 9)
RACE_MAX_MINUTES = 1440
# generate random fuel consumption
# the bigger the value, the longer the stints
fuel = random.randint(230, 625)
tires = random.randint(500, 1600)


### HELPER ###
def is_next_event_quali():
    """
    Checks if a file called 'next_event_is_quali' exists,
    and deletes it if it does.
    """
    exists = os.path.exists("next_event_is_quali")

    if exists:
        os.remove("next_event_is_quali")
    else:
        with open("next_event_is_quali", "w") as file:
            pass

    return exists


### MAIN ###

quali = is_next_event_quali()
print(quali)
if quali:
    commands = [
        "/broadcast Setting up Qualifying",
        "/race.raceMode = Hotlapping",
        f"/race.maxLaps = {QUALI_LAPS}",
        f"/race.maxMinutes = {QUALI_MAX_MINUTES}",
        "/race.startStyle = Countdown",
        "/race.ContactRules = EqualGhosts",
        "/fuel.fuelOn = 0",
        "/tireWear.tireWearOn = 0",
        # f"/fuelFullGasTime = {QUALI_FUEL}",
        # f"/tireWear.compound1Endurance = {QUALI_TIRES}",
        "/broadcast Hotlapping now, even if the User Interface might show different",
    ]
else:
    commands = [
        "/broadcast Setting up Race",
        "/race.raceMode = Race",
        f"/race.maxLaps = {race_laps}",
        f"/race.maxMinutes = {RACE_MAX_MINUTES}",
        "/race.startStyle = Random",
        "/race.ContactRules = Normal",
        "/fuel.fuelOn = 1",
        "/tireWear.tireWearOn = 1",
        f"/fuelFullGasTime = {fuel}",
        f"/tireWear.compound1Endurance = {tires}",
        "/broadcast Race now, even if the User Interface might show different",
    ]


print(commands)
with open("event_init_generated.src", "w", encoding="utf-8-sig") as file:
    file.write("\n".join(commands) + "\n")
