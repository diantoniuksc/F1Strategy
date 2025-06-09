import csv

input_file = 'all_years_sessions.csv'
output_file = 'all_years_sessions.csv' 

with open(input_file, 'r', encoding='utf-8') as file:
    data = file.read()

# Replace text
data = data.replace('alfa', 'sauber')

with open(output_file, 'w', encoding='utf-8') as file:
    file.write(data)
