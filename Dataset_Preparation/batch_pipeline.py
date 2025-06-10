import fastf1
from fastf1.events import get_event_schedule
import session_pipeline
import time

years_races = {2022: 22, 2023: 22, 2024: 24, 2025: 3}
session_type = 'R'
document_name = "all_years_sessions.csv"

def write_all_sessions_csv(year: int):
    if year not in years_races:
        print("Year is not correct")
        return 
    
    races_amount = years_races[year]
    print(races_amount)
    race_number = 1

    while race_number <= races_amount:
        session_pipeline.write_session_info(year, race_number, session_type, document_name)
        time.sleep(0.01)  # Sleep for 10 milliseconds
        race_number += 1

def write_all_years():
    for year in years_races:
        print(year)
        write_all_sessions_csv(year)

write_all_years()


