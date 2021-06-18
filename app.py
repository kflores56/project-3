from flask import Flask, render_template, redirect, request
# from xgboost import XGBClassifier
import pandas as pd
import numpy as np
import pickle

# Create an instance of Flask
app = Flask(__name__)

with open(f'xgb_model.pickle', "rb") as f:
    model = pickle.load(f)

feature_names = model.feature_names

# Route to render index.html template using data from Mongo
@app.route("/", methods=["GET", "POST"])
def home():
    output_message = ""

    if request.method == "POST":
        bedroom = float(request.form["bedroom"])
        bathroom = float(request.form["bathroom"])
        sqft = float(request.form["sqft"])
        yearBuilt = float(request.form["yearBuilt"])

        # data must be converted to df with matching feature names before predict
        data = pd.DataFrame(np.array([[bedroom, bathroom, sqft, yearBuilt]]), columns=feature_names)
        result = model.predict(data)
        if result == 1:
            output_message = "A home in Austin, TX will cost you XXX"
        else:
            output_message = "A home in Austin, TX will cost you XXX2"
    
    return render_template("index.html", message = output_message)

if __name__ == "__main__":
    app.run()