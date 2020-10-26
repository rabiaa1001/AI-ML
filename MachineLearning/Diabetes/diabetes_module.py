# Diabetes XGBoost Local Mode
#     Predict whether or not a person is at risk of developing diabetes
#     Data Prep technique used was just imputation with mean by each group based on diabetes class
#
#     XGBoost Training Parameters Source - https://xgboost.readthedocs.io/en/latest/parameter.html


import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import xgboost as xgb
from sklearn.metrics import classification_report, confusion_matrix
import pickle


# Files
column_list_file = './Files/diabetes_train_column_list.txt'
train_file = './Files/diabetes_train.csv'
validation_file = './Files/diabetes_validation.csv'

# Extract column files
with open(column_list_file, 'r') as f:
    columns = f.read().split(',')


df_train = pd.read_csv(train_file, names=columns)
df_validation = pd.read_csv(validation_file,names=columns)

# Remember to Flatten target to 1D array with ravel()
X_train = df_train.iloc[:,1:]
y_train = df_train.iloc[:,0].ravel()

X_valid = df_validation.iloc[:,1:]
y_valid = df_validation.iloc[:,0].ravel()

# Create the Classifier
classifier = xgb.XGBClassifier (objective="binary:logistic")

classifier.fit(X_train,
               y_train,
               eval_set = [(X_train, y_train), (X_valid, y_valid)],
               eval_metric=['logloss'],
               early_stopping_rounds=10)


y_predict = classifier.predict(X_valid)

# Confusion Matrix
print(classification_report(
    y_valid,
    y_predict,
    labels=[1,0],
    target_names=['Diabetic','Normal']))

# # Save the model
# filename = 'diabetes_xgboost_local_model.sav'
# pickle.dump(classifier, open(filename, 'wb'))

# loaded_diabetes_xgboost_local_model = pickle.load(open(filename, 'rb'))
# result = loaded_diabetes_xgboost_local_model.score(X_test, Y_test)
# print(result)
