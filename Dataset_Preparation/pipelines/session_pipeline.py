import csv
import fastf1
import name_to_compond
from fastf1.events import get_event_schedule

TRACK_LENGTHS = {
    'Bahrain': 5.412,
    'Saudi Arabian': 6.174,
    'Australian': 5.278,
    'Japanese': 5.807,
    'Chinese': 5.451,
    'Miami': 5.412,
    'Emilia Romagna': 4.909,
    'Monaco': 3.337,
    'Canadian': 4.361,
    'Spanish': 4.657,
    'Austrian': 4.326,
    'British': 5.891,
    'Hungarian': 4.381,
    'Belgian': 7.004,
    'Dutch': 4.259,
    'Italian': 5.793,
    'Azerbaijan': 6.003,
    'Singapore': 4.94,
    'United States': 5.513,
    'Mexico City': 4.304,
    'São Paulo': 4.309,
    'Las Vegas': 6.201,
    'Qatar': 5.419,
    'Abu Dhabi': 5.281,
    'French': 5.842
}


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

    # Get race length (number of laps)
    race_length = laps['LapNumber'].max()

    # Open a CSV file to write stint information
    with open(doc_name, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        # Write the header row
        #csv_writer.writerow(['driver_id', 'team_id', 'race_name', 'year', 'compound', 'stint_start_lap', 'tyre_life', 'race_length', 'is_valid'])

        prev_lap_tyre_age = None
        prev_lap_driver = None
        stint_start_lap = None
        last_lap = None

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

                circut_length = TRACK_LENGTHS[race_name.removesuffix(' Grand Prix')]

                # Write the stint info to the CSV file (using race_name)
                csv_writer.writerow([
                    #prev_lap_driver, team_name, race_name, year, race_length, tyre_name, stint_start_lap, prev_lap_tyre_age
                    prev_lap_driver, circut_length, year, tyre_name, prev_lap_tyre_age  
                ])

                stint_start_lap = lap['LapNumber']

            # Update previous lap variables for the next iteration
            prev_lap_tyre_age = tyre_life
            prev_lap_driver = driver_id
            last_lap = lap

        # After the loop, flush the last stint for the last driver
        if last_lap is not None and stint_start_lap is not None:
            tyre_name = last_lap['Compound']
            team_name = ''
            driver_row = results[results['Abbreviation'] == prev_lap_driver]
            if not driver_row.empty:
                team_name = driver_row.iloc[0]['TeamId']
            compound_code = name_to_compond.get_compound(year, race_number, tyre_name)
            csv_writer.writerow([
               prev_lap_driver, circut_length, year, tyre_name, prev_lap_tyre_age  
            ])
            



if __name__ == '__main__':
    # Example usage
    write_session_info(2025, 9, 'R', 'Dataset_Preparation/DataSetTest/session_test_v10.csv')