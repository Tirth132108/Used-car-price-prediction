import pandas as pd
import numpy as np
import sklearn
import joblib
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import (FunctionTransformer, OneHotEncoder, StandardScaler)
from sklearn.model_selection import (BaseCrossValidator, GridSearchCV, KFold,StratifiedKFold, train_test_split, ShuffleSplit, cross_val_score)
from numpy import absolute
import mlflow
import mlflow.sklearn
import logging
logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)
import dvc.api
from flask import Flask, render_template, redirect, request
app = Flask(__name__)

columns = ['Name','Location','Year','Kilometers_Driven','Fuel_Type','Transmission','Owner_Type','Mileage','Engine','Power','Seats']

model = joblib.load("ml_pipeline") 

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods =['POST', 'GET'])
def data():
    if request.method == 'POST':
        Name = request.form['Name']
        Location = request.form['Location']
        Year = int(request.form['Year'])
        Kilometers_Driven = int(request.form['Kilometers_Driven'])
        Fuel_Type = request.form['Fuel_Type']
        Transmission = request.form['Transmission']
        Owner_Type = request.form['Owner_Type']
        Mileage = request.form['Mileage']
        Engine = str(request.form['Engine'])
        Seats = request.form['Seats']
        Engine = Engine.split(' ')
        Engine = Engine[0]
        Engine = float(Engine)
        current_year = 2022
        Age = current_year - Year
        features = [[Location,Age,Kilometers_Driven,Fuel_Type,Transmission,Owner_Type,Mileage,Engine,Seats]]
        df = pd.DataFrame(features, columns=['Location', 'Age','Kilometers_Driven','Fuel_Type','Transmission','Owner_Type','Mileage','Engine','Seats'])
        prediction = model.predict(df)
        prediction = round(np.exp(prediction[0]),2)
        print(prediction)

    return render_template("index.html", prediction=prediction)




if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True,host='0.0.0.0', port=80)

