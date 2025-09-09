from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import pickle

app = Flask(__name__)

# Load scaler and model (replace file names with your actual saved files)
with open('scaler.pkl', 'rb') as f_scaler:
    scaler = pickle.load(f_scaler)

    model = joblib.load('logistic_regression_trained.pkl')

# The expected features in exact order, matching the HTML form inputs
FEATURES = [
    'radius_mean',
    'texture_mean',
    'perimeter_mean',
    'area_mean',
    'concavity_mean',
    'smoothness_mean',
    'concave_points_mean',
    'radius_worst',
    'perimeter_worst',
    'area_worst'
]

@app.route('/')
def home():
    # Render your HTML page (place the HTML file in a templates folder as 'index.html')
    return render_template('canc.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    print("Input data:", data)  # Debug line to confirm keys and values received
    try:
        input_features = [float(data[feature]) for feature in FEATURES]
        input_scaled = scaler.transform([input_features])
        prediction = model.predict(input_scaled)[0]
        result = 'Malignant' if prediction == 1 else 'Benign'

        return jsonify({'status': 'success', 'prediction': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
