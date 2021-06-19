from flask import Flask, render_template, redirect, request
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
# from http.server import HTTPServer
import pandas as pd
import numpy as np
# import pickle

housing = pd.read_csv("austinHousingData.csv")

X = housing[["yearBuilt", "livingAreaSqFt", "numOfBathrooms", "numOfBedrooms"]]
y = housing["latestPrice"].values.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

model = LinearRegression()
model.fit(X, y)

# Create an instance of Flask
app = Flask(__name__)

# with open(f'xgb_model.pickle', "rb") as f:
#     model = pickle.load(f)

# feature_names = model.predict(X)
# print("----Feature----")
# print(feature_names)
# print("--------")

# Route to render index.html template
# @app.route("/")
# def home():
#     return render_template('index.html')

@app.route("/", methods=["GET", "POST"])
def index():
    # output_message = ""

    if request.method == "POST":
        bedroom = float(request.form["bedroom"])
        bathroom = float(request.form["bathroom"])
        sqft = float(request.form["sqft"])
        yearBuilt = float(request.form["yearBuilt"])

        # data must be converted to df with matching feature names before predict
        data = pd.DataFrame(np.array([[bedroom, bathroom, sqft, yearBuilt]]))

        print("---Data---")
        print(data)
        print("------")
        result = model.predict(data)
        if result > 0:
            output_message = "A home in Austin, TX will cost you"
        else:
            output_message = "A home in Austin, TX will cost you XXX2"
    else:
        output_message = 'Try Again'
    
    return output_message
    # return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)