import csv
import numpy as np

input_file = 'Dataset_Preparation/DataSetTest/session_test_v10.csv'
output_file = 'Dataset_Preparation/DataSetTest/session_test_v10.csv'


def normalize_team_name():
    with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
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
        reader = list(csv.reader(file))
        header = reader[0]
        data_rows = reader[1:]

    # Collect tyre_life values as floats for IQR calculation
    tyre_life_values = [float(row[6]) for row in data_rows if row[6] not in ('', None)]
    Q1 = np.percentile(tyre_life_values, 25)
    Q3 = np.percentile(tyre_life_values, 75)
    IQR = Q3 - Q1
    lower_bound = max(7, Q1 - 1.5 * IQR)
    upper_bound = Q3 + 1.5 * IQR

    # Prepare header (add is_valid if not present)
    if 'is_valid' not in header:
        header.append('is_valid')
    rows.append(header)

    for row in data_rows:
        # Mark as valid if compound is not '0'
        is_valid = '1' if row[4] != '0' else '0'
        # Also mark as invalid if tyre_life is an outlier
        try:
            tyre_life = float(row[6])
            if not (lower_bound <= tyre_life <= upper_bound):
                is_valid = '0'
        except Exception:
            is_valid = '0'
        # Add or update is_valid column
        if len(row) == len(header) - 1:
            row.append(is_valid)
        else:
            row[7] = is_valid
        rows.append(row)

    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


#find_invalid_rows()

def remove_wet_tyres():
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        header = reader[0]
        data_rows = reader[1:]

    filtered_rows = []
    for row in data_rows:
        if row[3] != 'WET' and row[3] != 'UNKNOWN' and row[3] != 'INTERMEDIATE':
            filtered_rows.append(row)
        else:
            print('Removed row:' + str(row))

    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(filtered_rows)

if __name__ == "__main__":
    remove_wet_tyres()

def normalize_gp_name():
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()

    data = data.replace('ã', 'a')

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)

#normalize_gp_name()
