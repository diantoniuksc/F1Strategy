from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import training_data as td
import training_data_comp_num as tdcn
import pandas as pd

# --- Using One-Hot Encoded Compound (td) ---

x_train1, x_test1, y_train1, y_test1 = td.get_training_data(True, 1)

# Debug: Check compound columns in training data
compound_cols = [col for col in x_train1.columns if col.startswith('compound_')]
print("\nCompound columns in training data:", compound_cols)
print("First 10 rows of compound columns:")
print(x_train1[compound_cols].head(10))
print("Sum of each compound column in training data:")
print(x_train1[compound_cols].sum())
print("Target variable describe:")
print(y_train1.describe())

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


feature_list = x_train2.columns.tolist()
importances = list(rf2.feature_importances_)

#TODO: remove stint_start_lap    year
print('FEATURE NUM')
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]


# Example: create a new sample (fill with actual values as needed)
sample = pd.DataFrame([{
    'driver_id': 'VER',
    #'team_id': 'red_bull',
    'race_name': 'Japanese Grand Prix',
    'year': 2025,
    'compound': 'HARD',
    'stint_start_lap': 22.0,
}])

# One-hot encode categorical columns as in training
categorical_cols = ['driver_id', 'race_name', 'compound']
numeric_cols = [col for col in sample.columns if col not in categorical_cols]
sample_cat = pd.get_dummies(sample[categorical_cols])
sample_num = sample[numeric_cols]
sample_encoded = pd.concat([sample_num, sample_cat], axis=1)
sample_encoded = sample_encoded.reindex(columns=x_train1.columns, fill_value=0)

# Predict tyre life using the OHE compound model
predicted_tyre_life = rf1.predict(sample_encoded)
print("Predicted tyre life (OHE Compound):", predicted_tyre_life[0])

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.max_colwidth', None)
print("Encoded sample 1 for prediction:")
print(sample_encoded)

print("Sample features (nonzero/True):")
for col, val in sample_encoded.iloc[0].items():
    if val != 0:
        print(f"{col}: {val}")

# Example: create a new sample for the numeric compound model (fill with actual values as needed)
sample2 = pd.DataFrame([{
    'driver_id': 'VER',
   # 'team_id': 'red_bull',
    'race_name': 'Japanese Grand Prix',
    'year': 2025,
    'compound': 5, 
    'stint_start_lap': 1.0,
}])

# Align columns with training data (numeric compound version)
sample2 = sample2.reindex(columns=x_train2.columns, fill_value=0)

# Predict tyre life using the numeric compound model
predicted_tyre_life2 = rf2.predict(sample2)
print("Predicted tyre life (Numeric Compound):", predicted_tyre_life2[0])

# After fitting rf1 and making predictions:
result = permutation_importance(
    rf1, x_test1, y_test1.values.ravel(), n_repeats=10, random_state=42, n_jobs=-1
)

perm_sorted_idx = result.importances_mean.argsort()[::-1]
print("\nPermutation Feature Importance (OHE):")
for idx in perm_sorted_idx:
    print(f"{x_train1.columns[idx]:20} {result.importances_mean[idx]:.4f}")

# Optionally, plot the permutation importances
plt.figure(figsize=(10, 4))
plt.barh(x_train1.columns[perm_sorted_idx], result.importances_mean[perm_sorted_idx])
plt.xlabel("Permutation Importance")
plt.title("Permutation Feature Importance (OHE)")
plt.tight_layout()
plt.show()