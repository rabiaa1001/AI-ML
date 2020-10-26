{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Diabetes XGBoost Local Mode\n",
    "    Predict whether or not a person is at risk of developing diabetes\n",
    "    Data Prep technique used was just imputation with mean by each group based on diabetes class\n",
    "    \n",
    "    XGBoost Training Parameters Source - https://xgboost.readthedocs.io/en/latest/parameter.html"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting package metadata (current_repodata.json): done\n",
      "Solving environment: done\n",
      "\n",
      "# All requested packages already installed.\n",
      "\n"
     ]
    }
   ],
   "source": [
    "# Command to install the below commands\n",
    "# !conda install -c anaconda scikit-learn\n",
    "!conda install -y -c conda-forge xgboost"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sys\n",
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import itertools\n",
    "import xgboost as xgb\n",
    "from sklearn.metrics import classification_report, confusion_matrix\n",
    "import pickle\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [],
   "source": [
    "column_list_file = './Files/diabetes_train_column_list.txt'\n",
    "train_file = './Files/diabetes_train.csv'\n",
    "validation_file = './Files/diabetes_validation.csv'\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "## Added in and made some changes for Kaggle Submission"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# test_file = './diabetes-classification/test.csv'\n",
    "# submission_file = './diabetes-classification/sample_submission.csv'\n",
    "# kaggle_train_file = './diabetes-classification/train.csv'\n",
    "\n",
    "# test = pd.read_csv(test_file,index_col = 'p_id')\n",
    "# train = pd.read_csv(kaggle_train_file,index_col = 'p_id')\n",
    "# submission = pd.read_csv(submission_file,index_col = 'p_id')\n",
    "\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Extract Training, Validation files and Columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['diabetes_class',\n",
       " 'preg_count',\n",
       " 'glucose_concentration',\n",
       " 'diastolic_bp',\n",
       " 'triceps_skin_fold_thickness',\n",
       " 'two_hr_serum_insulin',\n",
       " 'bmi',\n",
       " 'diabetes_pedi',\n",
       " 'age']"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "with open(column_list_file,'r') as f:\n",
    "    columns = f.read().split(',')\n",
    "    \n",
    "columns\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(537, 9)\n",
      "(231, 9)\n"
     ]
    }
   ],
   "source": [
    "\n",
    "df_train = pd.read_csv(train_file, names=columns)\n",
    "\n",
    "df_validation = pd.read_csv(validation_file,names=columns)\n",
    "print(df_train.shape)\n",
    "\n",
    "print(df_validation.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(537, 8)\n",
      "(537,)\n",
      "(231, 8)\n",
      "(231,)\n"
     ]
    }
   ],
   "source": [
    "# Remember to Flatten target to 1D array with ravel()\n",
    "X_train = df_train.iloc[:,1:]\n",
    "y_train = df_train.iloc[:,0].ravel()\n",
    "\n",
    "X_valid = df_validation.iloc[:,1:]\n",
    "y_valid = df_validation.iloc[:,0].ravel()\n",
    "\n",
    "print(X_train.shape)\n",
    "print(y_train.shape)\n",
    "\n",
    "print(X_valid.shape)\n",
    "print(y_valid.shape)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "XGBClassifier(base_score=None, booster=None, colsample_bylevel=None,\n",
       "              colsample_bynode=None, colsample_bytree=None, gamma=None,\n",
       "              gpu_id=None, importance_type='gain', interaction_constraints=None,\n",
       "              learning_rate=None, max_delta_step=None, max_depth=None,\n",
       "              min_child_weight=None, missing=nan, monotone_constraints=None,\n",
       "              n_estimators=100, n_jobs=None, num_parallel_tree=None,\n",
       "              random_state=None, reg_alpha=None, reg_lambda=None,\n",
       "              scale_pos_weight=None, subsample=None, tree_method=None,\n",
       "              validate_parameters=None, verbosity=None)"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "classifier = xgb.XGBClassifier (objective=\"binary:logistic\")\n",
    "classifier"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[0]\tvalidation_0-logloss:0.49731\tvalidation_1-logloss:0.53781\n",
      "Multiple eval metrics have been passed: 'validation_1-logloss' will be used for early stopping.\n",
      "\n",
      "Will train until validation_1-logloss hasn't improved in 10 rounds.\n",
      "[1]\tvalidation_0-logloss:0.38423\tvalidation_1-logloss:0.43889\n",
      "[2]\tvalidation_0-logloss:0.31019\tvalidation_1-logloss:0.38287\n",
      "[3]\tvalidation_0-logloss:0.25777\tvalidation_1-logloss:0.34811\n",
      "[4]\tvalidation_0-logloss:0.21643\tvalidation_1-logloss:0.32662\n",
      "[5]\tvalidation_0-logloss:0.18654\tvalidation_1-logloss:0.31760\n",
      "[6]\tvalidation_0-logloss:0.16496\tvalidation_1-logloss:0.30746\n",
      "[7]\tvalidation_0-logloss:0.14842\tvalidation_1-logloss:0.29776\n",
      "[8]\tvalidation_0-logloss:0.13510\tvalidation_1-logloss:0.29316\n",
      "[9]\tvalidation_0-logloss:0.12093\tvalidation_1-logloss:0.29512\n",
      "[10]\tvalidation_0-logloss:0.10942\tvalidation_1-logloss:0.28657\n",
      "[11]\tvalidation_0-logloss:0.10401\tvalidation_1-logloss:0.28426\n",
      "[12]\tvalidation_0-logloss:0.09509\tvalidation_1-logloss:0.28488\n",
      "[13]\tvalidation_0-logloss:0.08787\tvalidation_1-logloss:0.28503\n",
      "[14]\tvalidation_0-logloss:0.08324\tvalidation_1-logloss:0.28639\n",
      "[15]\tvalidation_0-logloss:0.07746\tvalidation_1-logloss:0.28680\n",
      "[16]\tvalidation_0-logloss:0.07268\tvalidation_1-logloss:0.29116\n",
      "[17]\tvalidation_0-logloss:0.06895\tvalidation_1-logloss:0.29062\n",
      "[18]\tvalidation_0-logloss:0.06488\tvalidation_1-logloss:0.28669\n",
      "[19]\tvalidation_0-logloss:0.06190\tvalidation_1-logloss:0.28737\n",
      "[20]\tvalidation_0-logloss:0.05825\tvalidation_1-logloss:0.28534\n",
      "[21]\tvalidation_0-logloss:0.05564\tvalidation_1-logloss:0.28472\n",
      "Stopping. Best iteration:\n",
      "[11]\tvalidation_0-logloss:0.10401\tvalidation_1-logloss:0.28426\n",
      "\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,\n",
       "              colsample_bynode=1, colsample_bytree=1, gamma=0, gpu_id=-1,\n",
       "              importance_type='gain', interaction_constraints='',\n",
       "              learning_rate=0.300000012, max_delta_step=0, max_depth=6,\n",
       "              min_child_weight=1, missing=nan, monotone_constraints='()',\n",
       "              n_estimators=100, n_jobs=0, num_parallel_tree=1, random_state=0,\n",
       "              reg_alpha=0, reg_lambda=1, scale_pos_weight=1, subsample=1,\n",
       "              tree_method='exact', validate_parameters=1, verbosity=None)"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "classifier.fit(X_train,\n",
    "               y_train, \n",
    "               eval_set = [(X_train, y_train), (X_valid, y_valid)], \n",
    "               eval_metric=['logloss'],\n",
    "               early_stopping_rounds=10)\n",
    "\n",
    "               "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'validation_0': {'logloss': [0.497314,\n",
       "   0.384231,\n",
       "   0.310187,\n",
       "   0.257765,\n",
       "   0.216435,\n",
       "   0.186544,\n",
       "   0.164964,\n",
       "   0.148422,\n",
       "   0.135098,\n",
       "   0.120925,\n",
       "   0.109419,\n",
       "   0.104005,\n",
       "   0.095093,\n",
       "   0.087871,\n",
       "   0.083241,\n",
       "   0.077463,\n",
       "   0.07268,\n",
       "   0.068947,\n",
       "   0.064882,\n",
       "   0.061904,\n",
       "   0.058246]},\n",
       " 'validation_1': {'logloss': [0.537808,\n",
       "   0.438888,\n",
       "   0.382873,\n",
       "   0.348106,\n",
       "   0.326625,\n",
       "   0.317599,\n",
       "   0.30746,\n",
       "   0.297761,\n",
       "   0.293163,\n",
       "   0.295117,\n",
       "   0.286569,\n",
       "   0.284259,\n",
       "   0.284876,\n",
       "   0.285029,\n",
       "   0.286391,\n",
       "   0.286797,\n",
       "   0.291159,\n",
       "   0.290621,\n",
       "   0.286691,\n",
       "   0.287366,\n",
       "   0.285339]}}"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "evaluate_result = classifier.evals_result()\n",
    "evaluate_result # Checking format\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "range(0, 21)"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "rounds = range(len(evaluate_result['validation_0']['logloss']))\n",
    "rounds"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "plt.scatter(x = rounds, y = evaluate_result['validation_0']['logloss'], label = 'Training Error')\n",
    "plt.scatter(x = rounds, y = evaluate_result['validation_1']['logloss'], label = 'Validation Error')\n",
    "plt.xlabel('Iterations')\n",
    "plt.ylabel('Logloss')\n",
    "plt.title('Training and Validation Error')\n",
    "plt.legend()\n",
    "plt.grid(True)\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Check which features are the most important"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<matplotlib.axes._subplots.AxesSubplot at 0x11d689d10>"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "xgb.plot_importance(classifier)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>diabetes_class</th>\n",
       "      <th>preg_count</th>\n",
       "      <th>glucose_concentration</th>\n",
       "      <th>diastolic_bp</th>\n",
       "      <th>triceps_skin_fold_thickness</th>\n",
       "      <th>two_hr_serum_insulin</th>\n",
       "      <th>bmi</th>\n",
       "      <th>diabetes_pedi</th>\n",
       "      <th>age</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>1.000</td>\n",
       "      <td>130.0</td>\n",
       "      <td>70.0</td>\n",
       "      <td>13.000000</td>\n",
       "      <td>105.000000</td>\n",
       "      <td>25.9</td>\n",
       "      <td>0.472</td>\n",
       "      <td>22</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>8.000</td>\n",
       "      <td>133.0</td>\n",
       "      <td>72.0</td>\n",
       "      <td>22.164179</td>\n",
       "      <td>100.335821</td>\n",
       "      <td>32.9</td>\n",
       "      <td>0.270</td>\n",
       "      <td>39</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>3.298</td>\n",
       "      <td>137.0</td>\n",
       "      <td>68.0</td>\n",
       "      <td>14.000000</td>\n",
       "      <td>148.000000</td>\n",
       "      <td>24.8</td>\n",
       "      <td>0.143</td>\n",
       "      <td>21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0</td>\n",
       "      <td>2.000</td>\n",
       "      <td>88.0</td>\n",
       "      <td>74.0</td>\n",
       "      <td>19.000000</td>\n",
       "      <td>53.000000</td>\n",
       "      <td>29.0</td>\n",
       "      <td>0.229</td>\n",
       "      <td>22</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1</td>\n",
       "      <td>9.000</td>\n",
       "      <td>130.0</td>\n",
       "      <td>70.0</td>\n",
       "      <td>22.164179</td>\n",
       "      <td>100.335821</td>\n",
       "      <td>34.2</td>\n",
       "      <td>0.652</td>\n",
       "      <td>45</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   diabetes_class  preg_count  glucose_concentration  diastolic_bp  \\\n",
       "0               0       1.000                  130.0          70.0   \n",
       "1               1       8.000                  133.0          72.0   \n",
       "2               0       3.298                  137.0          68.0   \n",
       "3               0       2.000                   88.0          74.0   \n",
       "4               1       9.000                  130.0          70.0   \n",
       "\n",
       "   triceps_skin_fold_thickness  two_hr_serum_insulin   bmi  diabetes_pedi  age  \n",
       "0                    13.000000            105.000000  25.9          0.472   22  \n",
       "1                    22.164179            100.335821  32.9          0.270   39  \n",
       "2                    14.000000            148.000000  24.8          0.143   21  \n",
       "3                    19.000000             53.000000  29.0          0.229   22  \n",
       "4                    22.164179            100.335821  34.2          0.652   45  "
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_validation.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>preg_count</th>\n",
       "      <th>glucose_concentration</th>\n",
       "      <th>diastolic_bp</th>\n",
       "      <th>triceps_skin_fold_thickness</th>\n",
       "      <th>two_hr_serum_insulin</th>\n",
       "      <th>bmi</th>\n",
       "      <th>diabetes_pedi</th>\n",
       "      <th>age</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1.0</td>\n",
       "      <td>130.0</td>\n",
       "      <td>70.0</td>\n",
       "      <td>13.0</td>\n",
       "      <td>105.0</td>\n",
       "      <td>25.9</td>\n",
       "      <td>0.472</td>\n",
       "      <td>22</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   preg_count  glucose_concentration  diastolic_bp  \\\n",
       "0         1.0                  130.0          70.0   \n",
       "\n",
       "   triceps_skin_fold_thickness  two_hr_serum_insulin   bmi  diabetes_pedi  age  \n",
       "0                         13.0                 105.0  25.9          0.472   22  "
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "valid_X = df_validation.iloc[:,1:]\n",
    "valid_X.iloc[:1,:]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0,\n",
       "       0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0,\n",
       "       1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0,\n",
       "       1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,\n",
       "       1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0,\n",
       "       0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0,\n",
       "       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0,\n",
       "       0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0,\n",
       "       0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0,\n",
       "       0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,\n",
       "       1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1])"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "results = classifier.predict(valid_X)\n",
    "results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "df_validation['predicted_class'] = results"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>diabetes_class</th>\n",
       "      <th>preg_count</th>\n",
       "      <th>glucose_concentration</th>\n",
       "      <th>diastolic_bp</th>\n",
       "      <th>triceps_skin_fold_thickness</th>\n",
       "      <th>two_hr_serum_insulin</th>\n",
       "      <th>bmi</th>\n",
       "      <th>diabetes_pedi</th>\n",
       "      <th>age</th>\n",
       "      <th>predicted_class</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>1.000</td>\n",
       "      <td>130.0</td>\n",
       "      <td>70.0</td>\n",
       "      <td>13.000000</td>\n",
       "      <td>105.000000</td>\n",
       "      <td>25.9</td>\n",
       "      <td>0.472</td>\n",
       "      <td>22</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>8.000</td>\n",
       "      <td>133.0</td>\n",
       "      <td>72.0</td>\n",
       "      <td>22.164179</td>\n",
       "      <td>100.335821</td>\n",
       "      <td>32.9</td>\n",
       "      <td>0.270</td>\n",
       "      <td>39</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0</td>\n",
       "      <td>3.298</td>\n",
       "      <td>137.0</td>\n",
       "      <td>68.0</td>\n",
       "      <td>14.000000</td>\n",
       "      <td>148.000000</td>\n",
       "      <td>24.8</td>\n",
       "      <td>0.143</td>\n",
       "      <td>21</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0</td>\n",
       "      <td>2.000</td>\n",
       "      <td>88.0</td>\n",
       "      <td>74.0</td>\n",
       "      <td>19.000000</td>\n",
       "      <td>53.000000</td>\n",
       "      <td>29.0</td>\n",
       "      <td>0.229</td>\n",
       "      <td>22</td>\n",
       "      <td>0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1</td>\n",
       "      <td>9.000</td>\n",
       "      <td>130.0</td>\n",
       "      <td>70.0</td>\n",
       "      <td>22.164179</td>\n",
       "      <td>100.335821</td>\n",
       "      <td>34.2</td>\n",
       "      <td>0.652</td>\n",
       "      <td>45</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   diabetes_class  preg_count  glucose_concentration  diastolic_bp  \\\n",
       "0               0       1.000                  130.0          70.0   \n",
       "1               1       8.000                  133.0          72.0   \n",
       "2               0       3.298                  137.0          68.0   \n",
       "3               0       2.000                   88.0          74.0   \n",
       "4               1       9.000                  130.0          70.0   \n",
       "\n",
       "   triceps_skin_fold_thickness  two_hr_serum_insulin   bmi  diabetes_pedi  \\\n",
       "0                    13.000000            105.000000  25.9          0.472   \n",
       "1                    22.164179            100.335821  32.9          0.270   \n",
       "2                    14.000000            148.000000  24.8          0.143   \n",
       "3                    19.000000             53.000000  29.0          0.229   \n",
       "4                    22.164179            100.335821  34.2          0.652   \n",
       "\n",
       "   age  predicted_class  \n",
       "0   22                0  \n",
       "1   39                1  \n",
       "2   21                0  \n",
       "3   22                0  \n",
       "4   45                1  "
      ]
     },
     "execution_count": 18,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df_validation.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "              precision    recall  f1-score   support\n",
      "\n",
      "    Diabetic       0.85      0.78      0.82        79\n",
      "      Normal       0.89      0.93      0.91       152\n",
      "\n",
      "    accuracy                           0.88       231\n",
      "   macro avg       0.87      0.86      0.86       231\n",
      "weighted avg       0.88      0.88      0.88       231\n",
      "\n"
     ]
    }
   ],
   "source": [
    "print(classification_report(\n",
    "    df_validation['diabetes_class'],\n",
    "    df_validation['predicted_class'],\n",
    "    labels=[1,0],\n",
    "    target_names=['Diabetic','Normal']))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
