import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def get_training_data():
    training_data = pd.read_csv("Dataset_Preparation/data_processed/all_years_comp_v5.csv")
    # Print the 2nd row for debugging
    if len(training_data) > 1:
        print("2nd row of dataset:", training_data.iloc[1])
    else:
        print("Dataset has less than 2 rows.")

    # Use only features present in all_years_comp_v5.csv
    # Features: driver_id, race_length, year, compound, stint_start_lap, tyre_life, is_valid
    # One-hot encode driver_id and compound
    training_data_encoded = pd.get_dummies(training_data, columns=['driver_id', 'compound'])

    # Features for X: race_length, year, stint_start_lap, plus OHE columns
    feature_cols = [col for col in training_data_encoded.columns if col not in ['tyre_life', 'is_valid']]
    x = training_data_encoded[feature_cols]
    y = training_data_encoded[['tyre_life']]

    # If no samples, return empty splits
    if len(x) == 0 or len(y) == 0:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # Print whether each split is empty and their contents if not
    for name, df in zip(["x_train", "x_test", "y_train", "y_test"], [x_train, x_test, y_train, y_test]):
        if df.empty:
            print(f"{name} is empty.")
        else:
            print(f"{name} contents:")
            print(df)

    return x_train, x_test, y_train, y_test

# Call the function
#x_train, x_test, y_train, y_test = get_training_data(1)

#fix calls of functions in the randomforest doc