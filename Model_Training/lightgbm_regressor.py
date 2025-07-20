import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load data
df = pd.read_csv('Dataset_Preparation/all_years_comp_v5.csv', encoding='utf-8')

training_data = df[df['is_valid'].astype(str) == '1'] 

categorical_cols = ['driver_id', 'compound']


training_data = pd.get_dummies(training_data, columns=categorical_cols) 

x = training_data.drop(columns=['tyre_life', 'is_valid'])
y = training_data[['tyre_life']]

# Split data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train LightGBM regressor
model = LGBMRegressor(random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

print(f'RMSE: {rmse:.4f}')
print(f'R2 Score: {r2:.4f}')
print('Filtered rows:', training_data.shape[0])
