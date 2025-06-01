import os
import sys

# Ensure the app directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from ml.model_training import REAL_ESTATE_DATA_PATH, TARGET_COLUMN
from ml.real_estate_model import RealEstateModel

import mlflow


load_dotenv(
    dotenv_path="dbr/.env",
) 
print(f"Loaded env variabe {os.getenv('DATABRICKS_SERVER_HOSTNAME')}")

# Set up MLflow tracking URI and experiment

# Set access token
os.environ["DATABRICKS_TOKEN"] = os.getenv("DATABRICKS_ACCESS_TOKEN")
os.environ["DATABRICKS_HOST"] = f"https://{os.getenv("DATABRICKS_SERVER_HOSTNAME")}"

mlflow.set_tracking_uri("databricks")
mlflow.set_experiment("/Users/carlleeladefoged@gmail.com/RealEstateModelExperiment")
mlflow.set_registry_uri("databricks-uc")

# Get data
model = RealEstateModel(REAL_ESTATE_DATA_PATH)
X_train, X_test, y_train, y_test = model.split_data(TARGET_COLUMN)


# Autolog
mlflow.autolog()

with mlflow.start_run():
    # Train
    model.train_model(X_train, y_train)
    trained_model = model.model

    predictions = model.predict(X_test)
    r2_score = model.evaluate_model(X_test, y_test)

    # Log parameters and metrics
    mlflow.log_param("target_column", TARGET_COLUMN)
    mlflow.log_metric("r2_score", r2_score)

    # Log model
    # mlflow.sklearn.log_model(trained_model, "model", registered_model_name="RealEstateModel")
    mlflow.register_model(
        "runs:/{}/model".format(mlflow.active_run().info.run_id),
        "workspace.default.real_estate_model"
    )


    print("Model training and logging completed successfully.")




