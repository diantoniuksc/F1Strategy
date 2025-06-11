import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

training_data = pd.read_csv("Dataset_Preparation/all_years_sessions.csv")

# Filter for valid rows only
training_data = training_data[training_data['is_valid'] == 1]

# One-hot encode categorical columns
categorical_cols = ['driver_id', 'team_id', 'compound']
training_data_encoded = pd.get_dummies(training_data, columns=categorical_cols)

#training_data_encoded.info()

x = training_data_encoded.drop(columns=['tyre_life', 'is_valid'])
y = training_data_encoded[['tyre_life']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

linear_model = LinearRegression()
linear_model.fit(x_train, y_train)

print(linear_model.coef_)

predictions = linear_model.predict(x_test)
'''plt.scatter(y_test, predictions)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Actual vs Predicted Tyre Life")
plt.show()'''

#125.92828872331333
print(metrics.mean_squared_error(y_test, predictions))