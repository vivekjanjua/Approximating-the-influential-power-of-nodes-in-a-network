import sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.linear_model import LinearRegression
import os
import sys
import pickle

data = pd.DataFrame()
opt = sys.argv[1]
opt = int(opt)
file = os.listdir("done/")

for xl_file in file:
	data = data.append(pd.read_excel("done/"+xl_file),ignore_index = True)

data = data.sample(frac=1)
data.columns = ['Nd','Dg','Cq','Cc','H1','Sn']

data['Dg*Cc'] = data['Dg']*data['Cc']
data['H1*Cc'] = data['H1']*data['Cc']

y = data["Sn"].values
X = data.drop(columns="Sn")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

X_train = X_train.drop(columns="Nd")
temp = X_test['Nd'].values
X_test = X_test.drop(columns="Nd")

if(opt == 1):
	parameters = {'fit_intercept':[True,False], 'normalize':[True,False], 'copy_X':[True, False]}

	lin_model = LinearRegression(n_jobs = 8)

	gs = GridSearchCV(lin_model,parameters,cv=6,scoring="neg_mean_squared_error")
	gs.fit(X_train,y_train)
	with open('linear_mod.pkl','wb') as f:
			pickle.dump(gs,f)
else:
	with open('linear_mod.pkl','rb') as f:				#ye cheez karni hai use karne ke liye isse oickle imoort karlio
		gs = pickle.load(f)

y_test_predict = gs.predict(X_test)
y_test_predict = y_test_predict.round().astype(int)

delta = y_test - y_test_predict
delta = pd.DataFrame({"Node":temp.flatten(),"Actual":y_test.flatten(),"Predicted":y_test_predict.flatten(),"Difference":delta.flatten()})
np.savetxt("wiki-Vote+deg_cc.txt",delta.values,fmt="%d")