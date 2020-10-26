filename = 'diabetes_xgboost_local_model.sav'
pickle.dump(classifer, open(filename, 'wb'))

# loaded_diabetes_xgboost_local_model = pickle.load(open(filename, 'rb'))
# result = loaded_diabetes_xgboost_local_model.score(X_test, Y_test)
# print(result)
