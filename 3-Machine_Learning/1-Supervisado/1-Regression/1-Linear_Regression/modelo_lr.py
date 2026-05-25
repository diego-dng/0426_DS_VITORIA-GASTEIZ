# importing librarires
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import pickle

USA_Housing = pd.read_csv("data/USA_Housing.csv")

# Columns as Features
X = USA_Housing[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
       'Avg. Area Number of Bedrooms', 'Area Population']]
y = USA_Housing["Price"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state= 11)

print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)


lm = LinearRegression()
lm.fit(X_train, y_train)

with open("modelo_lm.pkl", "wb") as f:
    pickle.dump(lm, f)
