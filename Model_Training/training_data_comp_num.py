import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

def get_training_data_comp_num(weight_coef_compound: int):
    training_data = pd.read_csv("Dataset_Preparation/all_years_sessions_comp_num.csv")

    # Filter for valid rows only
    training_data = training_data[training_data['is_valid'] == 1]

    # One-hot encode categorical columns
    #categorical_cols = ['driver_id', 'team_id', 'race_name']
    categorical_cols = ['race_name']
    training_data_encoded = pd.get_dummies(training_data, columns=categorical_cols)

    # Give more weight to tyre compound columns
    '''compound_cols = [(col for col in training_data_encoded.columns if col=='compound')]
    for col in compound_cols:
        training_data_encoded[col] *= weight_coef_compound'''

    x = training_data_encoded.drop(columns=['tyre_life', 'is_valid', 'stint_start_lap', 'year', 'driver_id', 'team_id'])
    y = training_data_encoded[['tyre_life']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    return x_train, x_test, y_train, y_test

# Call the function
#x_train, x_test, y_train, y_test = get_training_data(3)