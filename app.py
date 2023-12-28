import os
import numpy as np
import pickle
from flask import Flask, render_template, request

model = pickle.load(open("model.pkl", "rb"))
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_diabetes():
    preg = request.form.get("pregnancies")
    glucose = request.form.get("glucose")
    bp = request.form.get("bloodPressure")
    skinthick = request.form.get("skinThickness")
    insulin = request.form.get("insulin")
    bmi = request.form.get("bmi")
    diab_pedi = request.form.get("diabetesPedigreeFunction")
    age = request.form.get("age")

    # prediction
    result = model.predict(
        np.array(
            [preg, glucose, bp, skinthick, insulin, bmi, diab_pedi, age], dtype=float
        ).reshape(1, -1)
    )

    if result[0] == 1:
        result = "Person is Diabetic"
    else:
        result = "Person is non Diabetic"

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
