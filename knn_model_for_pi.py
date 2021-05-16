import numpy as np
import pandas as pd 
from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale 
from sklearn import model_selection
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import BaggingRegressor

the_data = pd.read_csv('iot_project_setdata.csv')

del the_data['latitude']
del the_data['longitude']
del the_data['elevation']
del the_data['status']
del the_data['field4']
del the_data['entry_id']
del the_data['created_at']

df = the_data.rename(columns = {"field1":"Temperature","field2":"Humidity","field3":"Air Quality"})

x = df.drop("Air Quality", axis =1)
y = df["Air Quality"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3,random_state =42)

knn_tuned = KNeighborsRegressor(n_neighbors = 7)

knn_tuned.fit(x_train, y_train)

import joblib
filename = 'knn_model2.sav'
joblib.dump(knn_tuned, filename)
