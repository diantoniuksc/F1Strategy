import pandas as pd
from sklearn.model_selection import train_test_split

# Replace with your CSV file path
input_csv = "Dataset_Preparation/all_years_sessions.csv"
train_csv = "Model_Training/train.csv"
test_csv = "Model_Training/test.csv"

# Read the CSV file
df = pd.read_csv(input_csv)

# Split the data: 80% train, 20% test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, shuffle=True)

# Save to new CSV files
train_df.to_csv(train_csv, index=False)
test_df.to_csv(test_csv, index=False)