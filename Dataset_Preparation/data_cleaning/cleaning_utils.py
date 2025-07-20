import csv
import numpy as np
import pandas as pd

def delete_n_random_rows(doc_file, compound, n):
    """
    Delete n random rows for a given compound from the CSV and save the result.
    Assumes 'compound' column exists.
    """
    df = pd.read_csv(doc_file, header=0)
    compound_rows = df[df['compound'] == compound]
    if len(compound_rows) < n:
        print(f"Not enough rows to delete: requested {n}, available {len(compound_rows)}")
        return
    drop_indices = compound_rows.sample(n=n, random_state=42).index
    df = df.drop(drop_indices)
    df.to_csv(doc_file, index=False)
    print(f"Deleted {n} random rows of compound '{compound}' and saved to {doc_file}")


def trim_data(doc_file, compound, lower_or_upper, how_mutch):
    """
    Trim data for a compound by removing a percentage from lower or upper bound of tyre_life.
    lower_or_upper: 'l' for lower, 'u' for upper.
    how_mutch: percentage to trim.
    """
    df = pd.read_csv(doc_file, header=0)
    if 'is_valid' in df.columns:
        df = df[df['is_valid'] == 1]
    else:
        print(f"'is_valid' column not found in {doc_file}")
        return
    if lower_or_upper == 'l':
        min_value_old = pd.to_numeric(df.loc[df['compound'] == compound, 'tyre_life']).min()
        min_value_new = min_value_old + min_value_old * (how_mutch / 100)
        filtered_rows = []
        for _, row in df.iterrows():
            if (row['compound'] != compound) or (row['compound'] == compound and row['tyre_life'] >= min_value_new):
                filtered_rows.append(row.to_dict())
        df = pd.DataFrame(filtered_rows)
    elif lower_or_upper == 'u':
        max_value_old = pd.to_numeric(df.loc[df['compound'] == compound, 'tyre_life']).max()
        max_value_new = max_value_old - max_value_old * (how_mutch / 100)
        filtered_rows = []
        for _, row in df.iterrows():
            if (row['compound'] != compound) or (row['compound'] == compound and row['tyre_life'] <= max_value_new):
                filtered_rows.append(row.to_dict())
        df = pd.DataFrame(filtered_rows)
    else:
        print("Invalid option for lower_or_upper. Use 'l' or 'u'.")
        return
    df.to_csv(doc_file, index=False)
    print(f"Data trimmed and saved to {doc_file}")


def find_invalid_rows(input_file, output_file):
    """
    Mark rows as valid/invalid based on tyre life IQR for each compound.
    Adds/updates 'is_valid' column. Only keeps valid rows in output.
    Assumes compound is at index 5 and tyre_life at index 7.
    """
    rows = []
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        header = reader[0]
        data_rows = reader[1:]

    # Add 'is_valid' to header if missing
    if 'is_valid' not in header:
        header.append('is_valid')
    rows.append(header)

    compound_names = set(row[5] for row in data_rows)
    tyre_life_limits = {}

    # Calculate IQR bounds for each compound
    for name in compound_names:
        compound_rows = [row for row in data_rows if row[5] == name]
        lifes_for_compound = [float(row[7]) for row in compound_rows]
        Q1 = np.percentile(lifes_for_compound, 25)
        Q3 = np.percentile(lifes_for_compound, 75)
        IQR = Q3 - Q1
        lower_bound = Q1
        upper_bound = Q3 + 1.5 * IQR
        tyre_life_limits[name] = (lower_bound, upper_bound)

    for row in data_rows:
        try:
            compound_name = row[5]
            tyre_life_val = float(row[7])
            compound_min, compound_max = tyre_life_limits.get(compound_name)
            is_valid = '1' if (compound_min <= tyre_life_val <= compound_max) else '0'
        except Exception:
            is_valid = '0'

        # Add or update is_valid column
        if len(row) == len(header) - 1:
            row.append(is_valid)
        else:
            row[3] = is_valid

        if is_valid == '1':
            rows.append(row)

    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


def remove_wet_tyres(input_file, output_file):
    """
    Remove rows with wet, unknown, or intermediate tyres.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        header = reader[0]
        data_rows = reader[1:]

    filtered_rows = []
    for row in data_rows:
        if row[3] not in ['WET', 'UNKNOWN', 'INTERMEDIATE']:
            filtered_rows.append(row)

    with open(output_file, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(filtered_rows)


def normalize_team_name(input_file, output_file):
    """
    Normalize team names in the dataset.
    """
    with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
        data = file.read()
    data = data.replace('alfa', 'sauber')
    data = data.replace('alphatauri', 'racing_bulls')
    data = data.replace('rb', 'racing_bulls')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)


def normalize_gp_name(input_file, output_file):
    """
    Normalize Grand Prix names in the dataset.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        data = file.read()
    data = data.replace('\u00e3', 'a')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)



import csv
import numpy as np

input_file = 'Dataset_Preparation/DataSetTest/session_test_v9.csv'
output_file = 'Dataset_Preparation/DataSetTest/session_test_v9.csv'

def select_valid():
    with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
        data = list(csv.reader(file))

    header = data[0]
    data_rows = data[1:]

    data_rows = [row for row in data_rows if int(row[7]) == 1]

    with open(output_file, 'w', encoding='utf-8', errors='replace', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data_rows)

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


def change_name_for_length():
    with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
        data = list(csv.reader(file))

    header = data[0]
    data_rows = data[1:]

    for row in data_rows:
        row[2] = str(TRACK_LENGTHS[row[2].removesuffix(' Grand Prix')])

    with open(output_file, 'w', encoding='utf-8', errors='replace', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data_rows)


def remove_feature(indx):
    with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
        data = list(csv.reader(file))

    header = data[0]
    data_rows = data[1:]

    del header[indx]

    for row in data_rows:
        del row[indx]

    with open(output_file, 'w', encoding='utf-8', errors='replace', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data_rows)


if __name__ == '__main__':
    #select_valid()
    change_name_for_length()
    remove_feature(0)
