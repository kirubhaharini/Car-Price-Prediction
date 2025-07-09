# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import pickle

# Initialize app
app = Flask(__name__)

# Load trained model and hash encoder
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
hash_encoder = pickle.load(open('hash_encoder.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # --- Numerical Inputs ---
            Year = int(request.form['Year'])
            Engine = float(request.form['Engine'])
    
            ftcap = float(request.form['Fuel Tank Capacity'])
            mp = float(request.form['Max Power (bhp)'])
            mt = float(request.form['Max Torque (Nm)'])

            # --- Binary Inputs ---
            Transmission_Manual = 1 if request.form['Transmission_Manual'] == 'Yes' else 0
            Drivetrain_FWD = 1 if request.form['Drivetrain_FWD'] == 'Yes' else 0

    
            # --- Combine all features ---
            df = pd.DataFrame([{ 
                'Year': 2025 - Year,  # Age
                'Engine': Engine,
                'Fuel Tank Capacity': ftcap,
                'Max Power (bhp)': mp,
                'Max Torque (Nm)': mt,
                'Transmission_Manual': Transmission_Manual,
                'Drivetrain_FWD': Drivetrain_FWD
            }])


            # --- Predict and convert log price back ---
            prediction = model.predict(df)
            print(prediction)
            output = round(np.expm1(prediction[0]), 2)

            if output < 0:
                msg = "Sorry, this car can't be sold. Predicted Price: {} Rupees".format(output)
            else:
                msg = "Estimated Resale Price: {} Rupees".format(output)

            return render_template('index.html', prediction_text=msg)

        except Exception as e:
            return render_template('index.html', prediction_text="Error in prediction: {}".format(str(e)))

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
