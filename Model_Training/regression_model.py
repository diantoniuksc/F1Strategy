import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import training_data as td

x_train, x_test, y_train, y_test = td.get_training_data()

if x_train.empty or y_train.empty:
    print("ERROR: Training data is empty. Check your dataset and preprocessing steps.")
else:
    linear_model = LinearRegression()
    linear_model.fit(x_train, y_train)
    print(linear_model.coef_)
    predictions = linear_model.predict(x_test)
    plt.scatter(y_test, predictions)
    plt.xlabel("Actual Tyre Life")
    plt.ylabel("Predicted Tyre Life")
    plt.title("Actual vs Predicted Tyre Life")
    plt.show()
    print(metrics.mean_squared_error(y_test, predictions))

