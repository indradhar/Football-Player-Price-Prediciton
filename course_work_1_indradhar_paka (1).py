# -*- coding: utf-8 -*-
"""Course work 1_Indradhar Paka.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GvyTAYu4T1Hf06dJc27DBv4mTTGP0b6b
"""

import torch
torch.cuda.is_available()
device=torch.device("cuda:0")
device
if torch.cuda.is_available():
  device=torch.device("cuda:0")
  print("running on gpu")
else:
  device=torch.device("cpu")
  print("running on cpu")

torch.cuda.device_count()

"""1. Use Seaborn to investigate the data and present your findings"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

data = pd.read_csv("/content/Predicting the Price of a Football Player.csv")

type(data)

data

data['fpl_sel'] = data['fpl_sel'].replace('%','',regex=True).astype('float')/10

output_var = 'market_value'

import numpy as np
X = data[data.columns[~data.columns.isin([output_var])]]
y = data[[output_var]]

from sklearn.model_selection import train_test_split
np.random.seed(37) # Set seed
x_train, x_test = train_test_split(X, test_size = 0.25)

## dont using iloc as we have projected from data
y_train = y.loc[x_train.index.values] 
y_test = y.loc[x_test.index.values]
x_train = X.loc[x_train.index.values, :]
x_test = X.loc[x_test.index.values, :]

concat_train_data = pd.concat([x_train,y_train],axis=1)

concat_train_data.describe()

concat_train_data.corr()[output_var].sort_values()

concat_train_data.dtypes

import seaborn as sns
sns.boxplot(y='position',x=output_var,data=concat_train_data,orient='h')
plt.xlabel("Market Value")
plt.show()

sns.boxplot(y='position',x='market_value',data=concat_train_data,hue='new_signing',orient='h')
plt.xlabel("Market Value")
plt.show()

encoded_data = pd.get_dummies(concat_train_data, columns=["new_foreign","big_club","new_signing"],drop_first=True)

encoded_data.head()

concat_train_data.corr()[output_var].sort_values()

corr = concat_train_data.corr()
import seaborn as sns
import numpy as np
sns.heatmap(corr, mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(240,10,as_cmap=True),
            square=True)

corr

import seaborn as sns
sns.pairplot(encoded_data,height=2.5);

encoded_data.head()

"""2. Build models using all the algorithms above to predict market_value"""

data=data.drop(columns=['name'])
#make note of this..... cuz im removing from main data not from encoded

from sklearn import preprocessing
label_encoder=preprocessing.LabelEncoder()
encoded_data['club']=label_encoder.fit_transform(encoded_data['club'])
encoded_data['position']=label_encoder.fit_transform(encoded_data['position'])
encoded_data['nationality']=label_encoder.fit_transform(encoded_data['nationality'])

encoded_data=encoded_data.drop(columns=['name'])

encoded_data.head()

import numpy as np
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X = scaler.fit_transform(encoded_data[encoded_data.columns[~encoded_data.columns.isin([output_var])]])
Y = encoded_data[[output_var]]

encoded_data.corr()

x_test['club']=label_encoder.fit_transform(x_test['club'])
x_test['position']=label_encoder.fit_transform(x_test['position'])
x_test['nationality']=label_encoder.fit_transform(x_test['nationality'])
x_test=x_test.drop(columns=['name'])
x_train=encoded_data.drop(columns=['market_value'])

"""Linear Regression"""

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
Regression_Linear = LinearRegression(normalize=True)
print(Regression_Linear.get_params())
print(Regression_Linear.fit(x_train,y_train))
pred_linear = Regression_Linear.predict(x_test)
print("MSE score:",mean_squared_error(y_test,pred_linear))
print("R2 score:",r2_score(y_test,pred_linear))

pred_linear

"""Lasso Regression"""

from sklearn.linear_model import Lasso
model_lasso = Lasso(alpha=0.01)
model_lasso.fit(x_train, y_train) 
pred_lasso= model_lasso.predict(x_test)
print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_lasso)))
print("R2 score:",r2_score(y_test, pred_lasso))

pred_lasso

"""Ridge Regression"""

from sklearn.linear_model import Ridge
Rigression_Ridge = Ridge(alpha=0.01)
Rigression_Ridge.fit(x_train, y_train) 
pred_Ridge= Rigression_Ridge.predict(x_test)
print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_Ridge)))
print("R2 score:",r2_score(y_test, pred_Ridge))

pred_Ridge

"""Nearest Neighbour Regression"""

from sklearn import neighbors
from math import sqrt
rmse_val = []
for k in range(20):
    k = k+1
    model = neighbors.KNeighborsRegressor(n_neighbors = k)
    model.fit(x_train, y_train) 
    pred_neighbor=model.predict(x_test)
    error = sqrt(mean_squared_error(y_test,pred_neighbor))
    rmse_val.append(error) 
    print('RMSE value for k= ' , k , 'is:', error)

pred_neighbor

"""Support Vector Regression"""

from sklearn.svm import SVR
SupportVectorReg=SVR()
SupportVectorReg.fit(x_train,y_train)
pred_SVR=SupportVectorReg.predict(x_test)
print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_SVR)))
print("R2 score:",r2_score(y_test, pred_SVR))

pred_SVR

"""Tree Regression"""

from sklearn.tree import DecisionTreeRegressor
DecisionTreeReg=DecisionTreeRegressor()
DecisionTreeReg.fit(x_train,y_train)
pred_tree=DecisionTreeReg.predict(x_test)
print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_tree)))
print("R2 score:",r2_score(y_test, pred_tree))

pred_tree

"""Random Forest Regression """

from sklearn.ensemble import RandomForestRegressor
RandomForestReg=RandomForestRegressor()
RandomForestReg.fit(x_train,y_train)
pred_forest=RandomForestReg.predict(x_test)
print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_forest)))
print("R2 score:",r2_score(y_test, pred_forest))

pred_forest

"""Gradient Boosted Regression"""

from sklearn.ensemble import GradientBoostingRegressor
regressor = GradientBoostingRegressor(
    n_estimators= 500,
    max_depth= 4,
    min_samples_split= 5,
    learning_rate= 0.01,
)
regressor.fit(x_train,y_train)
pred_gradient = regressor.predict(x_test)
print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_gradient)))
print("R2 score:",r2_score(y_test,pred_gradient))

pred_gradient

"""3. Tune the hyperparameters and build the most accurate model"""

from sklearn.model_selection import GridSearchCV,RepeatedKFold,RandomizedSearchCV

"""For Linear Regression"""

model = LinearRegression()
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
space = dict()
space['fit_intercept'] = [True, False]
space['normalize'] = [True, False]
space['copy_X'] = [True, False]
search = GridSearchCV(model, space, scoring='neg_mean_absolute_error', n_jobs=1, cv=cv)
result = search.fit(x_train, y_train)
print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)
print('LinearRegression GridSearch Accuracy: %s' % result.best_estimator_.score(x_test,y_test))

"""Accurate model:"""

linearRegressor = LinearRegression(normalize=True,fit_intercept=False,copy_X=True)
linearRegressor.fit(x_train, y_train)
yPrediction = linearRegressor.predict(x_test)
print("RMSE score:",np.sqrt(mean_squared_error(y_test,yPrediction)))
print("R2 score:",r2_score(y_test,yPrediction))

"""For Lasso Regression"""

model = Lasso()
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
space = dict()
space['alpha'] = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100]
space['fit_intercept'] = [True, False]
space['normalize'] = [True, False]
space['max_iter'] = [1,10,50,100]
space['copy_X'] = [True, False]
space['warm_start'] = [True, False]
space['selection'] = ['cyclic', 'random']
space['precompute'] = [True, False,]
search = GridSearchCV(model, space, scoring='neg_mean_absolute_error', n_jobs=-1, cv=cv)
result = search.fit(x_train, y_train)

print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)
print('Lasso GridSearch Accuracy: %s' % result.best_estimator_.score(x_test,y_test))

"""Accurate Model:"""

model_lasso = Lasso(alpha=0.01,selection='random')
model_lasso.fit(x_train, y_train) 
pred_lasso= model_lasso.predict(x_test)
print("RMSE score:",np.sqrt(mean_squared_error(y_test,pred_lasso)))
print("R2 score:",r2_score(y_test, pred_lasso))

"""For Ridge Regression"""

model = Ridge()
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
space = dict()
space['solver'] =  ['svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga']
space['alpha'] = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100]
space['fit_intercept'] = [True, False]
space['normalize'] = [True, False]
space['max_iter'] = [1,10,50,100,500,1000]
space['copy_X'] = [True, False]
search = GridSearchCV(model, space, scoring='neg_mean_absolute_error', n_jobs=-1, cv=cv)
result = search.fit(x_train, y_train)

print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)
print('Ridge GridSearch Accuracy: %s' % result.best_estimator_.score(x_test,y_test))

"""Accurate Model:"""

rr = Ridge(alpha=1,solver = 'lsqr')
rr.fit(x_train, y_train) 
pred_rr= rr.predict(x_test)
print("RMSE score:",np.sqrt(mean_squared_error(y_test,pred_rr)))
print("R2 score:",r2_score(y_test, pred_rr))

"""For Nearest Neighbour Regression"""

model=neighbors.KNeighborsRegressor()

leaf_size = list(range(1,50))
n_neighbors = list(range(1,30))
p=[1,2]
hyperparameters = dict(leaf_size=leaf_size, n_neighbors=n_neighbors, p=p)

search = GridSearchCV(model, hyperparameters, cv=10)
result = search.fit(x_train, y_train)

print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)
print('Knn GridSearch Score: %s' % result.best_estimator_.score(x_test,y_test))

"""Accurate Model:"""

model = neighbors.KNeighborsRegressor(n_neighbors = 16,algorithm='kd_tree',p=1,weights='distance')
model.fit(x_train, y_train)  #fit the model
pred_knn=model.predict(x_test) #make prediction on test set
error = sqrt(mean_squared_error(y_test,pred_knn)) #calculate rmse

print('RMSE value :', error)
print("R2 score:",r2_score(y_test, pred_knn))

"""For Support Vector Regression"""

model = SVR()
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
space = dict()
space['max_iter'] = [1,10,50,100]
space['kernel']= ['linear','poly','rbf','sigmoid']
space['gamma'] = [1, 0.1, 0.01, 0.001, 0.0001]
space['C']: [0.1, 1, 10, 100, 1000]

search = GridSearchCV(model, space, scoring='neg_mean_absolute_error', n_jobs=-1, cv=cv)

result = search.fit(x_train, y_train)

print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)
print('SVR GridSearch Accuracy: %s' % result.best_estimator_.score(x_test,y_test))

"""Accurate Model:"""

'''
SVR()
SupportVectorReg=SVR(kernel='poly',gamma=1)
SupportVectorReg.fit(x_train,y_train)
pred_svr=SupportVectorReg.predict(x_test)

print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_svr)))
print("R2 score:",r2_score(y_test, pred_svr))
'''
SupportVectorReg=SVR()
SupportVectorReg.fit(x_train,y_train)
pred_SVR=SupportVectorReg.predict(x_test)
print("MSE score:",np.sqrt(mean_squared_error(y_test,pred_SVR)))
print("R2 score:",r2_score(y_test, pred_SVR))

"""For Tree Regression"""

model = DecisionTreeRegressor()
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
space = dict()
space['max_depth']= [None,1,2,3,4,5,6,7]
space['max_features']= [None, 'sqrt', 'auto', 'log2', 0.3,0.5,0.7 ]
space['min_samples_split']= [2,0.3,0.5]
space['min_samples_leaf']=[1, 0.3,0.5]
space['criterion'] = ['mse','friedman_mse','mae']
space['splitter'] = ['best','random']
search = GridSearchCV(model, space, scoring='neg_mean_absolute_error', n_jobs=-1, cv=cv)
result = search.fit(x_train, y_train)
print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)

"""Accurate Model:"""

DecisionTreeReg=DecisionTreeRegressor(criterion= 'friedman_mse', max_depth= 6, max_features= 'auto', min_samples_leaf= 1, min_samples_split= 2, splitter= 'random')
DecisionTreeReg.fit(x_train,y_train)
pred_tree=DecisionTreeReg.predict(x_test)
print("RMSE score:",np.sqrt(mean_squared_error(y_test,pred_tree)))
print("R2 score:",r2_score(y_test, pred_tree))

"""For Random Forest Regression"""

model = RandomForestRegressor()
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt','log2']
max_depth = [int(x) for x in np.linspace(10, 1000,10)]

min_samples_split = [2, 5, 10,14]
min_samples_leaf = [1, 2, 4,6,8]

random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf
              }
              
RF_RandomCv = RandomizedSearchCV(estimator=model,param_distributions=random_grid,n_iter=100,cv=3,verbose=2,
                               random_state=100,n_jobs=-1)
result=RF_RandomCv.fit(x_train,y_train)

print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)
print('Random Forest GridSearch Accuracy: %s' % result.best_estimator_.score(x_test,y_test))

"""Accurate Model:"""

RandomForestReg=RandomForestRegressor(max_depth=8, max_features='sqrt',n_estimators=200)
RandomForestReg.fit(x_train,y_train)
pred_forest=RandomForestReg.predict(x_test)
print("RMSE score:",np.sqrt(mean_squared_error(y_test,pred_forest)))
print("R2 score:",r2_score(y_test, pred_forest))

"""For Gradient Boosted Regression"""

model =GradientBoostingRegressor()
cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
space = dict()
space['n_estimators']= [200, 500]
space['max_features']= ['auto', 'sqrt', 'log2']
space['max_depth'] = [4,5,6,7,8]
space['alpha'] = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1, 10, 100,0.99]
space['loss'] = ['ls', 'lad', 'huber', 'quantile']
space['subsample'] = [1]
search = RandomizedSearchCV(model, space, scoring='neg_mean_absolute_error', n_jobs=-1, cv=cv)
result = search.fit(x_train, y_train)
print('Best Score: %s' % result.best_score_)
print('Best Hyperparameters: %s' % result.best_params_)

"""Accurate Model:"""

regressor = GradientBoostingRegressor(
    subsample =  1,
    n_estimators= 500, 
    max_features= 'log2', 
    max_depth= 5, 
    loss= 'lad', 
    alpha= 0.01
)
regressor.fit(x_train,y_train)
pred_gboost = regressor.predict(x_test)
print("RMSE score:",np.sqrt(mean_squared_error(y_test,pred_gboost)))
print("R2 score:",r2_score(y_test,pred_gboost))

"""4. Use model selection approaches discussed in class to choose the best model

From all the above models we can observe that the SUPPORT VECTOR REGRESSION, reports us the best results as the R2 value of the SVR is lowest among all other regressions. The Best Score of SVR is  -6.099489733412793, Best Hyperparameters: {'gamma': 0.0001, 'kernel': 'rbf', 'max_iter': 100}, Accuracy: 0.2185178234939857, MSE score: 10.47592874913882 and R2 score: 0.39691213061159725
So, Support vector Machine is the best algorithm among all others in this scenario. So we deployed Support Vector Machine Regression in Restful API.

5. Genetic Algorithm
"""

import csv
import random as rand
import math
import operator


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    # print('Distances: ')
    # print(*distances, sep=",")
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(min(k, len(distances))):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        #print('Neighbors: ' + neighbors[x][-1])
        #print(classVotes)
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    # print(classVotes)#coba1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct = correct+1
    return (correct / float(len(testSet))) * 100.0


def generateChromosome(chromosome):
    return [rand.randint(1, 100) for x in range(chromosome)]


def desimal(biner):
    return int(biner, 2)


def kNN(k, testSet, trainingSet):
    # generate predictions
    predictions = []
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        #print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
    accuracy = getAccuracy(testSet, predictions)
    #print('Accuracy: ' + repr(accuracy) + '%')
    return accuracy


def crossover(one, two):
    parent = [one, two]
    zero = '0'
    male = "{0:b}".format(parent[0])
    female = "{0:b}".format(parent[1])
    length = max(len(male), len(female))
    if length % 2 == 1:
        length = length + 1
    while len(male) < length:
        male = zero + male

    while len(female) < length:
        female = zero + female

    child = []
    half = int(length / 2)
    male1 = male[:half]
    male2 = male[half:]

    female1 = female[:half]
    female2 = female[half:]

    child.append(desimal(male1 + female2))
    child.append(desimal(female1 + male2))
    return child



# prepare data
trainingSet = x_train
testSet = x_test
split = 0.67

print('Train set: ' + repr(len(trainingSet)))
print('Test set: ' + repr(len(testSet)))

accResult = [[]]
chromosome = 10
population = generateChromosome(chromosome)

for x in range(len(population)):
  accResult.append([population[x], kNN(population[x], testSet, trainingSet)])

del accResult[0]

for x in range(200):
        status_one = True
        status_zero = True
        accResult = sorted(accResult, key=lambda l: l[1], reverse=True)
        newChromosome = crossover(accResult[0][0], accResult[1][0])
        for i in accResult:
            if newChromosome[0] == i[0]:
                status_zero = False;
            if newChromosome[1] == i[0]:
                status_one = False
        if status_zero:
            accResult.append([newChromosome[0], kNN(newChromosome[0], testSet, trainingSet)])
        if status_one:
            accResult.append([newChromosome[1], kNN(newChromosome[1], testSet, trainingSet)])

accResult = sorted(accResult, key=lambda l: l[1],reverse=True)
print("accuracy: \n")
print(accResult[0][1])

!pip install flask-ngrok

"""6. RESTFUL API"""

from flask_ngrok import run_with_ngrok
from flask import Flask

from flask import Flask, render_template, request, Response
app =Flask(__name__)

df = pd.read_csv('/content/Predicting the Price of a Football Player.csv')

df1=df
df1.drop(["name","club","position","nationality","fpl_sel"],axis='columns',inplace=True)

x=df1[df1.columns[~df1.columns.isin(["market_value"])]].to_numpy()
y=df1.market_value.to_numpy()
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size = 0.25)

run_with_ngrok(app)

@app.route("/" , methods=['GET','POST'])
def index():
    return render_template("ml_assignment.html")
@app.route("/data", methods=['GET','POST'])
def data():     
    if request.method == "POST":
         opt= request.form['excellent']
         m = int(opt)*1
         a= request.form['age']
         b= request.form['position_cat']
         c= request.form['page_views']
         d= request.form['fpl_value']
         e= request.form['fpl_points']
         f= request.form['region']
         g= request.form['new_foreign']
         h= request.form['age_cat']
         i= request.form['club_id']
         j= request.form['big_club']
         k= request.form['new_signing']
         li=[a,b,c,d,e,f,g,h,i,j,k]
         model=SVR()
         model.fit(x_train,y_train)
         y_pred_svr=model.predict(x_test)
         market_value=model.predict([li])
    return render_template("ml_data.html",market_value=market_value )

app.run()

!ngrok authtoken 1k2FFfPooTPMAKtuJFQ0iCleB2o_39Y3J6rSwnpkESb46Z7h3