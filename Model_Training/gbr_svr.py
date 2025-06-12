from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn import metrics
import matplotlib.pyplot as plt
import training_data as td


x_train, x_test, y_train, y_test = td.get_training_data()

gbr = GradientBoostingRegressor(n_estimators = 200)

gbr.fit(x_train, y_train.values.ravel())
gbr_predictions = gbr.predict(x_test)

'''plt.scatter(y_test, gbr_predictions)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Gradient Boosting: Actual vs Predicted Tyre Life")
plt.show()'''

print("Gradient Boosting MSE:", metrics.mean_squared_error(y_test, gbr_predictions))


svr = SVR()

svr.fit(x_train, y_train.values.ravel())
svr_predictions = svr.predict(x_test)

'''plt.scatter(y_test, svr_predictions)
plt.xlabel("Actual Tyre Life")
plt.ylabel("Predicted Tyre Life")
plt.title("Support Vector: Actual vs Predicted Tyre Life")
plt.show()'''

# 90.6651272277365
print("SVR MSE:", metrics.mean_squared_error(y_test, svr_predictions))



