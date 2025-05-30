import joblib
import pandas as pd
from flask import Flask, request, jsonify



ready_flag = False # Track when the app is ready for requests during init

# TODO: Implement logger logic

app = Flask(__name__)

# Load trained lr model
model = joblib.load('ml/models/linear_regression_real_estate_model.pkl')

@app.route('/health', methods=['GET'])
def get_health():
    """
    Health check to verify API is running.
    Returns a static OK response.
    """
    return jsonify({"status": "ok"}), 200

@app.route('/predict', methods=['POST'])
def post_predict():
    """
    Expects a JSON payload with the required features.
    Returns a prediction based on the loaded model.
    """
    if not ready_flag:
        return jsonify({"error": "Service not ready"}), 503

    data = request.get_json()
    
    # Request validate
    # TODO: Add attribute in RealEstateModel to get required features (yuck, hard-coded...)
    # X1 transaction date,X2 house age,X3 distance to the nearest MRT station,X4 number of convenience stores,X5 latitude,X6 longitude
    required_features = [
        "X1 transaction date",
        "X2 house age",
        "X3 distance to the nearest MRT station",
        "X4 number of convenience stores",
        "X5 latitude",
        "X6 longitude"
    ]
    missing_features = [feature for feature in required_features if feature not in data]
    if missing_features:
        return jsonify({"error": f"Missing features: {', '.join(missing_features)}"}), 400
    
    data_df = pd.DataFrame([data])
    
    # Make prediction
    prediction = model.predict(data_df)
    
    return jsonify({
        "prediction": prediction[0]
    }), 200


if __name__ == '__main__':
    try:
        ready_flag = True 
        app.run(port=8000, debug=True)
    except Exception as e:
        print(f"Error starting the app: {e}")
        ready_flag = False
        raise RuntimeError("Woops, failed to start the app") from e