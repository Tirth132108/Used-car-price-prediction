#prepared by : Tirth Patel(1206441) and Niyatiben Salot(1206446)

from colorama import Cursor
import pandas as pd
import numpy as np
import sklearn
from flaskext.mysql import MySQL
import mysql.connector
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

import mysql.connector

app = Flask(__name__)


 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="Car_Prediction"
)


#specifiying the features name and their key's values
columns = ['Name','Location','Year','Kilometers_Driven','Fuel_Type','Transmission','Owner_Type','Mileage','Engine','Power','Seats']
locations = ['Mumbai', 'Pune', 'Chennai', 'Coimbatore', 'Hyderabad', 'Jaipur',
       'Kochi', 'Kolkata', 'Delhi', 'Bangalore', 'Ahmedabad']


#loading pipeline that has been created
model = joblib.load("ml_pipeline") 

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods =['POST', 'GET'])
def data():
    if request.method == 'POST':
        #reading the data 
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
        Engine = Engine.split(' ') #Engine has values like 67 cc, separating 67
        Engine = Engine[0]
        Engine = float(Engine)
        current_year = 2022
        Age = current_year - Year # calculating new feature AGE

        cursor = mydb.cursor(dictionary=True, buffered=True)
    
        cursor.execute(''' INSERT INTO data (Name,Location,Year,Kilometers_Driven,Fuel_Type,Transmission,Owner_Type,Mileage,Engine,Seats) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',[Name,Location,Year,Kilometers_Driven,Fuel_Type,Transmission,Owner_Type,Mileage,Engine,Seats])
        mydb.commit()

        features = [[Location,Age,Kilometers_Driven,Fuel_Type,Transmission,Owner_Type,Mileage,Engine,Seats]]
        # creating dataframe
        df = pd.DataFrame(features, columns=['Location', 'Age','Kilometers_Driven','Fuel_Type','Transmission','Owner_Type','Mileage','Engine','Seats'])
        
        #making prediction
        prediction = model.predict(df)

        prediction = round(np.exp(prediction[0]),2) #having 2 numbers after decimal. 
       

    return render_template("index.html", prediction=prediction)




if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)

