# -*- coding: utf-8 -*-
"""A01_Machine_Learning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ABvmJHPZmm_8xWeQRP5qsGZvA1F1xuNg

Read the file "Scroe.csv".

Fill the Null or NA values with average of respective student.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier

df = pd.read_csv('Score.csv')

for index, row in df.iterrows():
    mean_score = row[3:].replace(0, np.nan).mean()
    df.iloc[index, 3:] = row[3:].replace(0, np.nan).fillna(mean_score)

"""Calculate Avgerage of Each student and store in the column named as "Avg"
"""

df['Avg'] = df.iloc[:, 3:].mean(axis=1)

"""On the basis of Average, calculate the progress of student.



```
if average > 5 then set progress to Good,
else if average == 5 then progress is average
else set progress to below average.
```


"""

def assign_progress(avg):
    if avg > 5:
        return 'Good'
    elif avg == 5:
        return 'average'
    else:
        return 'below average'

df['Progress'] = df['Avg'].apply(assign_progress)

"""Transform Categorical values into Numerical values."""

le = LabelEncoder()
df['Progress'] = le.fit_transform(df['Progress'])

non_numeric_columns = df.select_dtypes(exclude='number').columns

for column in non_numeric_columns:
    df[column] = le.fit_transform(df[column])

print("Columns in DataFrame:", df.columns)

if 'student_id' in df.columns:
    X = df.drop(columns=['student_id', 'Progress'])
else:
    X = df.drop(columns=['Progress'])

y = df['Progress']

"""Set the s to all the columns except s.no and progress.

Set the label variable to progress.

Split the dataset into test and train.
  1. 1st time train set is set to 70 and test 30
  2. For second time split into 0.20
  3. For third time split into 1:3

"""

def stratified_split(X, y, test_size=0.30):
    stratified_split = StratifiedKFold(n_splits=int(1 / test_size))
    for train_index, test_index in stratified_split.split(X, y):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        return X_train, X_test, y_train, y_test

X_train_70, X_test_30, y_train_70, y_test_30 = stratified_split(X, y, test_size=0.30)
X_train_80, X_test_20, y_train_80, y_test_20 = stratified_split(X, y, test_size=0.20)
X_train_75, X_test_25, y_train_75, y_test_25 = stratified_split(X, y, test_size=0.25)

"""Apply all the Machine algorithm we had covered in our course to predict the progress of student.

"""

def train_n_evaluate(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    return accuracy

models = {
    'Logistic Regression': LogisticRegression(),
    'Decision Tree': DecisionTreeClassifier(),
    'Random Forest': RandomForestClassifier()
}

results = {}

results['70-30'] = {name: train_n_evaluate(model, X_train_70, X_test_30, y_train_70, y_test_30) for name, model in models.items()}
results['80-20'] = {name: train_n_evaluate(model, X_train_80, X_test_20, y_train_80, y_test_20) for name, model in models.items()}
results['75-25'] = {name: train_n_evaluate(model, X_train_75, X_test_25, y_train_75, y_test_25) for name, model in models.items()}

for split, res in results.items():
    print(f"results for {split} split:")
    for model, accuracy in res.items():
        print(f"{model}: {accuracy}")

"""Self Learn:

Learn a new Machine Learning Algorithm Which is not covered in our course and implement it on our score dataset for the prediction of Progress of student.
"""

gbc = GradientBoostingClassifier()

results['70-30']['Gradient Boosting'] = train_n_evaluate(gbc, X_train_70, X_test_30, y_train_70, y_test_30)
results['80-20']['Gradient Boosting'] = train_n_evaluate(gbc, X_train_80, X_test_20, y_train_80, y_test_20)
results['75-25']['Gradient Boosting'] = train_n_evaluate(gbc, X_train_75, X_test_25, y_train_75, y_test_25)

for split, res in results.items():
    print(f"results for {split} split:")
    for model, accuracy in res.items():
        print(f"{model}: {accuracy}")

"""#Do's

For each model , use each spliting and get three different results.

Compare the all the model on each spliting.

Result : generate result on the basis of our your thinking.

Visualize your dataset on the each model using matplotlib.
"""

def plot_results(results):
    for split, res in results.items():
        plt.figure()
        plt.title(f"accuracy for {split} split")
        plt.bar(res.keys(), res.values())
        plt.xlabel('Model')
        plt.ylabel('accuracy')
        plt.ylim(0, 1)
        plt.show()

plot_results(results)