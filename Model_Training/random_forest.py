from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import matplotlib.pyplot as plt
import training_data as td
import training_data_comp_num as tdcn
import pandas as pd

# --- Using One-Hot Encoded Compound (td) ---
x_train1, x_test1, y_train1, y_test1 = td.get_training_data(3)

rf1 = RandomForestRegressor(n_estimators=90, random_state=42)
rf1.fit(x_train1, y_train1.values.ravel())
predictions1 = rf1.predict(x_test1)

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.scatter(y_test1, predictions1)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Random Forest (OHE Compound)")
print("OHE Compound MSE:", metrics.mean_squared_error(y_test1, predictions1))
print("OHE Compound MAE:", metrics.mean_absolute_error(y_test1, predictions1))
print("OHE Compound R2:", metrics.r2_score(y_test1, predictions1))

# --- Using Numeric Compound (tdcn) ---
x_train2, x_test2, y_train2, y_test2 = tdcn.get_training_data_comp_num(3)

x_train2.columns = x_train2.columns.astype(str)
x_test2.columns = x_test2.columns.astype(str)
rf2 = RandomForestRegressor(n_estimators=90, random_state=42)
rf2.fit(x_train2, y_train2.values.ravel())
predictions2 = rf2.predict(x_test2)

plt.subplot(1, 2, 2)
plt.scatter(y_test2, predictions2)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Random Forest (Numeric Compound)")
print("Numeric Compound MSE:", metrics.mean_squared_error(y_test2, predictions2))
print("Numeric Compound MAE:", metrics.mean_absolute_error(y_test2, predictions2))
print("Numeric Compound R2:", metrics.r2_score(y_test2, predictions2))

plt.tight_layout()
plt.show()



# Example: create a new sample (fill with actual values as needed)
sample = pd.DataFrame([{
    'driver_id': 'VER',
    'team_id': 'red_bull',
    'race_name': 'Canadian Grand Prix',
    'compound': 'C5',
    'stint_start_lap': 1.0,
}])

# One-hot encode categorical columns as in training
sample_encoded = pd.get_dummies(sample)

# Align columns with training data (OHE version)
sample_encoded = sample_encoded.reindex(columns=x_train1.columns, fill_value=0)

# Predict tyre life using the OHE compound model
predicted_tyre_life = rf1.predict(sample_encoded)
print("Predicted tyre life (OHE Compound):", predicted_tyre_life[0])



# Example: create a new sample for the numeric compound model (fill with actual values as needed)
sample2 = pd.DataFrame([{
    'driver_id': 'VER',
    'team_id': 'red_bull',
    'race_name': 'Canadian Grand Prix',
    'compound_num': 5, 
    'stint_start_lap': 1.0,
}])

# Align columns with training data (numeric compound version)
sample2 = sample2.reindex(columns=x_train2.columns, fill_value=0)

# Predict tyre life using the numeric compound model
predicted_tyre_life2 = rf2.predict(sample2)
print("Predicted tyre life (Numeric Compound):", predicted_tyre_life2[0])