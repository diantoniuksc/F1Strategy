import csv
import fastf1
import name_to_compond

def get_session_info(year: int, race_number: int, session_type: str):
    """
    Loads an F1 session, detects tyre stints for all drivers, and writes stint info to a CSV file.
    Each row in the CSV represents the end of a stint for a driver.
    """
    # Load the session using the round number (race_number) and session type (e.g., 'R' for Race)
    session = fastf1.get_session(year, race_number, session_type)
    session.load()

    # Get all laps and session results (for driver/team info)
    laps = session.laps
    results = session.results

    # Open a CSV file to write stint information
    with open('sessionstints.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        # Write the header row
        csv_writer.writerow(['driver_id', 'team_id', 'gp_number', 'year', 'compound', 'last_lap_number', 'tyre_life'])

        # Initialize variables to track the previous lap's tyre age and driver
        prev_lap_tyre_age = None
        prev_lap_driver = None

        # Iterate over all laps in the session
        for idx, lap in laps.iterrows():
            tyre_life = lap['TyreLife']
            driver_id = lap['Driver']

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
                last_lap_number = prev_lap['LapNumber']

                # Get the team ID for the previous driver from the results DataFrame
                team_name = ''
                driver_row = results[results['Abbreviation'] == prev_lap_driver]
                if not driver_row.empty:
                    team_name = driver_row.iloc[0]['TeamId']

                # Map the compound name to its code using your custom function
                compound_code = name_to_compond.get_compound(year, race_number, tyre_name)

                # Write the stint info to the CSV file
                csv_writer.writerow([
                    prev_lap_driver, team_name, race_number, year, compound_code, last_lap_number, prev_lap_tyre_age
                ])

            # Update previous lap variables for the next iteration
            prev_lap_tyre_age = tyre_life
            prev_lap_driver = driver_id

# Example usage: process the 2023 Bahrain Grand Prix race session
get_session_info(2023, 1, 'R')