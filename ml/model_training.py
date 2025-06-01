import os
import sys

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.real_estate_model import RealEstateModel

REAL_ESTATE_DATA_PATH = "data/Real estate.csv"
TARGET_COLUMN = "Y house price of unit area"

if __name__ == "__main__":
    # Training script for the real estate model
    model = RealEstateModel(REAL_ESTATE_DATA_PATH)

    X_train, X_test, y_train, y_test = model.split_data(TARGET_COLUMN)
    model.train_model(X_train, y_train)
    model.evaluate_model(X_test, y_test)
    predictions = model.predict(X_test)
    print("Predictions:", predictions[:5])  # Print first 5 predictions

    # Do some evaluation here if needed

    model.save_model("ml/models/linear_regression_real_estate_model.pkl")