from sklearn.neural_network import MLPRegressor
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import training_data_comp_num as tdcn
import pandas as pd

# --- Using Numeric Compound (tdcn) ---
x_train2, x_test2, y_train2, y_test2 = tdcn.get_training_data_comp_num(3)

x_train2.columns = x_train2.columns.astype(str)
x_test2.columns = x_test2.columns.astype(str)

# IMPORTANT: Scale the features for neural networks
scaler = StandardScaler()
x_train2_scaled = scaler.fit_transform(x_train2)
x_test2_scaled = scaler.transform(x_test2)

# Configure MLPRegressor with better parameters
mlp = MLPRegressor(
    hidden_layer_sizes=(100, 50, 25),  # Deeper network
    activation='relu',
    solver='adam',
    alpha=0.001,  # Regularization
    learning_rate_init=0.001,
    max_iter=2000,  # More iterations
    early_stopping=True,
    validation_fraction=0.1,
    random_state=42
)

mlp.fit(x_train2_scaled, y_train2.values.ravel())
predictions2 = mlp.predict(x_test2_scaled)

# Create proper plot figure
plt.figure(figsize=(8, 6))
plt.scatter(y_test2, predictions2, alpha=0.6)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("MLPRegressor (Numeric Compound) - Scaled Features")

# Add diagonal line for perfect predictions
plt.plot([y_test2.min(), y_test2.max()], [y_test2.min(), y_test2.max()], 'r--', lw=2)

print("Numeric Compound MSE:", metrics.mean_squared_error(y_test2, predictions2))
print("Numeric Compound MAE:", metrics.mean_absolute_error(y_test2, predictions2))
print("Numeric Compound R2:", metrics.r2_score(y_test2, predictions2))

plt.tight_layout()
plt.show()