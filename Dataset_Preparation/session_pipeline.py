import csv
import fastf1
import name_to_compond
from fastf1.events import get_event_schedule

def write_session_info(year: int, race_number: int, session_type: str, doc_name: str):
    """
    Loads an F1 session, detects tyre stints for all drivers, and writes stint info to a CSV file.
    Each row in the CSV represents the end of a stint for a driver.
    """
    # Get the race name from the event schedule
    schedule = get_event_schedule(year)
    event_row = schedule[schedule['RoundNumber'] == race_number]
    if not event_row.empty:
        race_name = event_row.iloc[0]['EventName']
    else:
        race_name = f"Round_{race_number}"

    # Load the session using the round number and session type (e.g., 'R' for Race)
    session = fastf1.get_session(year, race_number, session_type)
    session.load()

    # Get all laps and session results (for driver/team info)
    laps = session.laps
    results = session.results

    # Open a CSV file to write stint information
    with open(doc_name, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        # Write the header row
        #csv_writer.writerow(['driver_id', 'team_id', 'race_name', 'year', 'compound', 'stint_start_lap', 'tyre_life'])

        # Initialize variables to track the previous lap's tyre age and driver
        prev_lap_tyre_age = None
        prev_lap_driver = None
        stint_start_lap = None

        # Iterate over all laps in the session
        for idx, lap in laps.iterrows():
            tyre_life = lap['TyreLife']
            driver_id = lap['Driver']

            if (
                prev_lap_tyre_age is None and prev_lap_driver is None 
                and stint_start_lap is None
            ):
                stint_start_lap = lap['LapNumber']

            # Check if a new stint has started (either a driver change or tyre age reset)
            if (
                prev_lap_tyre_age is not None and prev_lap_driver is not None
                and (driver_id != prev_lap_driver or tyre_life != prev_lap_tyre_age + 1)
            ):
                # Find the position of the current lap in the DataFrame
                current_pos = laps.index.get_loc(idx)

                # Get the previous lap's data (end of the previous stint)
                prev_lap = laps.iloc[current_pos - 1]
                tyre_name = prev_lap['Compound']

                # Get the team ID for the previous driver from the results DataFrame
                team_name = ''
                driver_row = results[results['Abbreviation'] == prev_lap_driver]
                if not driver_row.empty:
                    team_name = driver_row.iloc[0]['TeamId']

                # Map the compound name to its code using your custom function
                compound_code = name_to_compond.get_compound(year, race_number, tyre_name)

                # Write the stint info to the CSV file (using race_name)
                csv_writer.writerow([
                    prev_lap_driver, team_name, race_name, year, compound_code, stint_start_lap, prev_lap_tyre_age
                ])
                print(f"Stint: {prev_lap_driver}, {team_name}, {race_name}, {year}, {compound_code}, {stint_start_lap}, {prev_lap_tyre_age}")

                stint_start_lap = lap['LapNumber']

            # Update previous lap variables for the next iteration
            prev_lap_tyre_age = tyre_life
            prev_lap_driver = driver_id

# Example usage
# write_session_info(2023, 7, 'R', 'Dataset_Preparation/session_test.csv')