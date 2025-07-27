from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import training_data as td
import pandas as pd

# --- Using One-Hot Encoded Compound (td) ---

x_train1, x_test1, y_train1, y_test1 = td.get_training_data()

compound_cols = [col for col in x_train1.columns if col.startswith('compound_')]
print("\nCompound columns in training data:", compound_cols)
print("First 10 rows of compound columns:")
print(x_train1[compound_cols].head(10))
print("Sum of each compound column in training data:")
print(x_train1[compound_cols].sum())
print("Target variable describe:")
if y_train1.empty or y_train1.shape[1] == 0 or x_train1.empty:
    print("ERROR: Training data is empty. Check your dataset and preprocessing steps.")
else:
    print(y_train1.describe())

rf1 = RandomForestRegressor(n_estimators=90, random_state=42)
rf1.fit(x_train1, y_train1.values.ravel())
import joblib
joblib.dump(rf1, 'rf_model_v5.joblib')
predictions1 = rf1.predict(x_test1)

plt.figure(figsize=(8, 6))
plt.scatter(y_test1, predictions1, alpha=0.6)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Random Forest: Actual vs Predicted Tyre Life")
plt.grid(True)
plt.show()
print("OHE Compound MSE:", metrics.mean_squared_error(y_test1, predictions1))
print("OHE Compound MAE:", metrics.mean_absolute_error(y_test1, predictions1))
print("OHE Compound R2:", metrics.r2_score(y_test1, predictions1))

feature_list = x_train1.columns.tolist()
importances = list(rf1.feature_importances_)

print('FEATURE OHE')
# Evaluate the stint_start_lap feature
if 'stint_start_lap' in feature_list:
    stint_index = feature_list.index('stint_start_lap')
    stint_importance = importances[stint_index]
    if stint_importance < 0.01:  # Threshold for negligible importance
        print("Removing stint_start_lap due to low importance:", stint_importance)
        x_train1 = x_train1.drop(columns=['stint_start_lap'])
        x_test1 = x_test1.drop(columns=['stint_start_lap'])
        feature_list.pop(stint_index)
        importances.pop(stint_index)
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]

plt.show()