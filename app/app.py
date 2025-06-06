import joblib
import pandas as pd
import logging
from flask import Flask, request, jsonify

model = None

# Init logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="app/app.log", level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Load trained lr model
def load_model(model_path='ml/models/linear_regression_real_estate_model.pkl'):
    model = joblib.load(model_path)
    logger.info("Model loaded successfully.")
    return model
model = load_model()

# Init Flask app
app = Flask(__name__)

# Controllers
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
    if not model:
        logger.error("Service not ready to handle requests")
        return jsonify({"error": "Service not ready"}), 503

    data = request.get_json()
    
    # Request validation
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
        logger.error(f"Missing features in request: {', '.join(missing_features)}")
        return jsonify({"error": f"Missing features: {', '.join(missing_features)}"}), 400
    
    # TODO: Null check!
    
    data_df = pd.DataFrame([data])
    
    # Make prediction
    prediction = model.predict(data_df)
    logger.info(f"Received data: {data}, Prediction: {prediction[0]}")

    return jsonify({
        "prediction": prediction[0]
    }), 200


if __name__ == '__main__':
    try:
        logger.info("Starting the Flask app...")
        app.run(port=8000, debug=True)
        logger.info("Flask app started successfully.")
        
    except Exception as e:
        print(f"Error starting the app: {e}")
        raise RuntimeError("Woops, failed to start the app") from e