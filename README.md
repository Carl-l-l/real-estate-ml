# Real Estate House Price Prediction Service

## Solution Overview

This project provides a REST API for predicting house prices based on real estate features. The solution includes:
- A trained linear regression model (see [`ml/`](ml/)) using the given housing dataset.
- A Flask-based API ([`app/app.py`](app/app.py)) with endpoints for health check and price prediction.
- Automated tests ([`tests/test_app.py`](tests/test_app.py)) to verify model loading and prediction.
- Containerization via Docker for easy deployment (Note: Still needs gunicorn implementation).

## Running the Code

### 1. Install Dependencies

All dependencies are listed in [`requirements.txt`](requirements.txt).  
Install with:

```sh
pip install -r requirements.txt
```

### 2. Train the model
To train the model, use script in the `ml/` directory:

```sh
python ml/model_training.py
```
This will generate a pickle model file in the [`ml/models/`](ml/models/) directory, which is used by the Flask app for loading the model and making predictions.

### 3. Run Flask App
```sh
python app/app.py
```

or use Flask CLI:
```sh
export FLASK_APP=app/app.py
flask run
```

### 4. Test the API
Run automated test to verify model loading and prediction:

```sh
python tests/test_app.py
```

### 5. Dockerize the Application
To build and run the Docker container, use the provided `Dockerfile`:

```sh
docker build -t 'realestateml:latest' .
docker run -p 8000:8000 realestateml:latest
```

### 6. Access the API
You can access the API at `http://localhost:8000/`.

### 7. API Endpoints
- **Health Check**: `GET /health`
  - Returns a simple health check response.
- **Predict Price**: `POST /predict`
  - Expects a JSON body with real estate features.
  - Returns the predicted house price.
### Example Request Body
```json
{
    "X1 transaction date": 2012.667,
    "X2 house age": 32.0,
    "X3 distance to the nearest MRT station": 84.9,
    "X4 number of convenience stores": 10.0,
    "X5 latitude": 24.982,
    "X6 longitude": 121.540
}
```

### Example Response
Please note it is predicted house price of unit area.
```json
{
    "prediction": 37.123456789
}
```