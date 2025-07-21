import fastf1
from fastf1.events import get_event_schedule
import Dataset_Preparation.normalization.name_to_compound as name_to_compound

# Set the year and event name for which you want to get the race number
"""year = 2024
event_name = 'Bahrain'
session = 'R'
driver_id = 'VER'"""


def get_driver_session_info(year: int, event_name: str, session: str, driver_id: str):
# Get the event schedule for the specified year
    schedule = get_event_schedule(year)

    # Try to find the event by name and extract the race number (round)
    race_info = schedule.get_event_by_name(event_name)
    if not race_info.empty:
        race_number = race_info['RoundNumber']
        print(f"Race number for '{event_name}' in {year} is: {race_number}")
    else:
        print(f"Event '{event_name}' not found in {year}.")
        race_number = None  # Set to None if not found

    # Only proceed if the race number was found
    if race_number is not None:
        # Load the race session for a different year/event as an example
        session = fastf1.get_session(year, event_name, session)
        session.load()

        # Get all laps from the session
        laps = session.laps

        # Select the fastest lap 
        fastest_lap = laps.pick_drivers(driver_id).pick_fastest()

        # Print the compound used on the fastest lap
        print(f"Fastest lap compound: {fastest_lap['Compound']}")

        # Print the compound mapping using your custom function
        compound_code = name_to_compound.get_compound(year, race_number, fastest_lap['Compound'])
        print(f"Compound code from mapping: {compound_code}")

        # Show the arguments used for mapping
        print(f"Mapping arguments: year={year}, race_number={race_number}, compound={fastest_lap['Compound']}")

        # Get team from session results
        results = session.results
        driver_row = results[results['Abbreviation'] == driver_id]
        if not driver_row.empty:
            team_name = driver_row.iloc[0]['TeamName']
            print(team_name)
    else:
        print("Skipping session analysis due to missing race number.")
