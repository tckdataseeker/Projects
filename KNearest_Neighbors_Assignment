#assignment on k-nearest neighbors in Python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('KNN_Project_Data')

#Create a StandardScaler() object called scaler.
scaler = StandardScaler()

#Fit scaler to the features.
scaler.fit(df.drop('TARGET CLASS',axis = 1))

#Use the .transform() method to transform the features to a scaled version.
scaled_features = scaler.transform(df.drop('TARGET CLASS',axis = 1))

#Convert the scaled features to a dataframe and check the head of this dataframe to make sure the scaling worked.
df_feat = pd.DataFrame(scaled_features, columns= df.columns[:-1])


#Use train_test_split to split data into a training set and a testing set.
X = df_feat
y = df['TARGET CLASS']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=101)


from sklearn.neighbors import KNeighborsClassifier

#Create a KNN model instance with n_neighbors=1
knn = KNeighborsClassifier(n_neighbors=1)

#Fit this KNN model to the training data.
knn.fit(X_train,y_train)

#Use the predict method to predict values using your KNN model and X_test.
pred = knn.predict(X_test)

#create a confusion matrix and classification report
from sklearn.metrics import confusion_matrix, classification_report
print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))


#come up with a new K-value

error_rate = []

for i in range(1,40):
    
    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred = knn.predict(X_test)
    error_rate.append(np.mean(pred != y_test))


# create the following plot using the information from your for loop.
plt.figure(figsize =(10,6))
plt.plot(range(1,40), error_rate,marker = 'o',linestyle = '--')

#use the new k-value obtained from visual observation of the graph produced above
knn = KNeighborsClassifier(n_neighbors=23)
knn.fit(X_train,y_train)
pred = knn.predict(X_test)

print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))
