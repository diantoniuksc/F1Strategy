from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

training_data = pd.read_csv("Dataset_Preparation/DataSetTest/length_comp_life_with_validity_edit2.csv")
training_data = training_data[training_data['is_valid'] == 1]
training_data = pd.get_dummies(training_data, columns=['compound'])

x = training_data.drop(columns=['tyre_life', 'is_valid'])
y = training_data[['tyre_life']]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)



rf_model = RandomForestRegressor(n_estimators=90, random_state=42)
rf_model.fit(x_train, y_train.values.ravel())

predictions = rf_model.predict(x_test)

# Feature importances for Random Forest
importances = rf_model.feature_importances_
feature_names = x_train.columns
importances_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
importances_df = importances_df.sort_values(by='importance', ascending=False)
print("\nRandom Forest Feature Importances:")
print(importances_df)

# Plot feature importances
plt.figure(figsize=(10, 5))
plt.bar(importances_df['feature'], importances_df['importance'])
plt.xticks(rotation=90)
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.title('Random Forest Feature Importances')
plt.tight_layout()
plt.show()

print("Mean Squared Error:", metrics.mean_squared_error(y_test, predictions))
print("Mean Absolute Error:", metrics.mean_absolute_error(y_test, predictions))
print("R-squared:", metrics.r2_score(y_test, predictions))

plt.scatter(y_test, predictions)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Actual vs Predicted Tyre Life")
#plt.show()


linear_model = LinearRegression()
linear_model.fit(x_train, y_train)

predictions_linear = linear_model.predict(x_test)

print("Linear Model Mean Squared Error:", metrics.mean_squared_error(y_test, predictions_linear))
print("Linear Model Mean Absolute Error:", metrics.mean_absolute_error(y_test, predictions_linear))
print("Linear Model R-squared:", metrics.r2_score(y_test, predictions_linear))

plt.scatter(y_test, predictions_linear)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Linear Model: Actual vs Predicted Tyre Life")
#plt.show()

print("x_train shape:", x_train.shape)
print("y_train describe:\n", y_train.describe())
print("x_train describe:\n", x_train.describe())
print("Unique values in y_train:", y_train['tyre_life'].unique())
print("First few rows of x_train:\n", x_train.head())
print(training_data[['compound_SOFT', 'compound_MEDIUM', 'compound_HARD']].sum())

for col in ['compound_SOFT', 'compound_MEDIUM', 'compound_HARD']:
    mean = training_data.loc[training_data[col]==1, 'tyre_life'].mean()
    std = training_data.loc[training_data[col]==1, 'tyre_life'].std()
    print(f"{col}: mean={mean:.2f}, std={std:.2f}")



sample = pd.DataFrame([{
    'circut_length': '5.807',
    #'team_id': 'red_bull',
    #'race_name': 'Japanese Grand Prix',
    #'year': 2025,
    'compound': 'HARD',
    #'stint_start_lap': 22.0,
}])

categorical_cols = ['compound']
numeric_cols = [col for col in sample.columns if col not in categorical_cols]
sample_cat = pd.get_dummies(sample[categorical_cols])
sample_num = sample[numeric_cols]
sample_encoded = pd.concat([sample_num, sample_cat], axis=1)
sample_encoded = sample_encoded.reindex(columns=x_train.columns, fill_value=0)

predicted_tyre_life = rf_model.predict(sample_encoded)
print("Predicted tyre life :", predicted_tyre_life[0])
