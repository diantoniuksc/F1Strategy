import csv

input_file = 'Dataset_Preparation/all_years_sessions.csv'
output_file = 'Dataset_Preparation/all_years_sessions.csv' 


def normalize_team_name():
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()

    data = data.replace('alfa', 'sauber')
    data = data.replace('alphatauri', 'racing_bulls')
    data = data.replace('rb', 'racing_bulls')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)

#normalize_team_name()

def find_invalid_rows():
    rows = []
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        # Add the new column to the header
        header.append('is_valid')
        rows.append(header)
        for row in reader:
            # Mark as valid if compound is not '0'
            is_valid = '1' if row[4] != '0' else '0' 
            row.append(is_valid)
            rows.append(row)

    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

find_invalid_rows()

def normalize_gp_name():
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()
        
    data = data.replace('ã', 'a')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)

#normalize_gp_name()