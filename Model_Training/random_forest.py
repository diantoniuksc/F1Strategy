import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn import metrics
import matplotlib.pyplot as plt

# Load data
training_data = pd.read_csv("Dataset_Preparation/all_years_sessions.csv")
training_data = training_data[training_data['is_valid'] == 1]

# One-hot encode categorical columns
categorical_cols = ['driver_id', 'team_id', 'race_name', 'compound']
training_data_encoded = pd.get_dummies(training_data, columns=categorical_cols)

x = training_data_encoded.drop(columns=['tyre_life', 'is_valid'])
y = training_data_encoded[['tyre_life']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train Random Forest
rf = RandomForestRegressor(n_estimators=90, random_state=42)
rf.fit(x_train, y_train.values.ravel())

# Predict
predictions = rf.predict(x_test)

# Plot
plt.scatter(y_test, predictions)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Random Forest: Actual vs Predicted Tyre Life")
plt.show()

# Print MSE
#45.3020875
print("Mean Squared Error:", metrics.mean_squared_error(y_test, predictions))