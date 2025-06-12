import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import training_data as td

x_train, x_test, y_train, y_test = td.get_training_data(3)

linear_model = LinearRegression()
linear_model.fit(x_train, y_train)

print(linear_model.coef_)

predictions = linear_model.predict(x_test)

plt.scatter(y_test, predictions)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Actual vs Predicted Tyre Life")
plt.show()

#125.92828872331333
#104.16281526580653 GPs as names OHEed
#67.71570635444589 removed outliers
print(metrics.mean_squared_error(y_test, predictions))

