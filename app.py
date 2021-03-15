import flask
from flask import Flask, render_template, url_for, request
import pickle
import sklearn

model = pickle.load(open("car_pred_model", "rb"))


app = Flask('__name__')


@app.route("/")
def home():
    return render_template("layout.html")


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    if request.method == "POST":
        present_price = float(request.form['Present_Price'])
        kms_driven = int(request.form['Kms_Driven'])
        owner = request.form['Owner']
        fuel_type = request.form['Fuel_type']
        if fuel_type == "Petrol":
            fuel_type_petrol = 1
            fuel_type_diesel = 0
        elif fuel_type == "Diesel":
            fuel_type_petrol = 0
            fuel_type_diesel = 1
        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 0
        year = int(request.form['Year'])
        year = 2020 - year
        seller_type = request.form['Seller_type']
        if seller_type == "Individual":
            seller_type_individual = 1
        else:
            seller_type_individual = 0
        transmission_type = request.form['Transmission_type']
        if transmission_type == 'Manual':
            transmission_manual = 1
        else:
            transmission_manual = 0
        prediction=model.predict([[present_price,kms_driven,owner,year,fuel_type_diesel,fuel_type_petrol, seller_type_individual, transmission_manual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('layout.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('layout.html', prediction_text="You Can Sell The Car at {}".format(output))

    else:
        return render_template('layout.html')


if __name__ == "__main__":
    app.run(debug=True)

