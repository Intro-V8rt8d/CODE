from flask import Flask, request, render_template, jsonify
import pickle
import joblib

app = Flask(__name__)

# Load model and scaler files - ensure these files are accessible when running app
model = joblib.load('logistic_regression_trained.pkl')
scaler = pickle.load(open('scaler.pkl', 'rb'))

FEATURES = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'concavity_mean',
    'smoothness_mean', 'concave points_mean', 'radius_worst', 'perimeter_worst',
    'area_worst'
]

@app.route('/')
def home():
    return render_template('canc.html')  # Your HTML page filename

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    try:
        # Extract features in the expected order
        input_features = [float(data[feature]) for feature in FEATURES]

        # Scale features with saved scaler
        input_scaled = scaler.transform([input_features])

        # Make prediction
        prediction = model.predict(input_scaled)[0]

        # Map prediction to readable labels
        result = 'Malignant' if prediction == 1 else 'Benign'

        return jsonify({'status': 'success', 'prediction': result})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)