from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import matplotlib.pyplot as plt
import training_data as td


x_train, x_test, y_train, y_test = td.get_training_data()

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