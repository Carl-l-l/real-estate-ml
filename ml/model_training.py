from real_estate_model import RealEstateModel

if __name__ == "__main__":
    # Training script for the real estate model

    real_estate_data_path = "data/Real estate.csv"
    model = RealEstateModel(real_estate_data_path)
    target_column = "Y house price of unit area"

    X_train, X_test, y_train, y_test = model.split_data(target_column)
    model.train_model(X_train, y_train)
    model.evaluate_model(X_test, y_test)
    predictions = model.predict(X_test)
    print("Predictions:", predictions[:5])  # Print first 5 predictions

    # Do some evaluation here if needed

    model.save_model("ml/models/linear_regression_real_estate_model.pkl")