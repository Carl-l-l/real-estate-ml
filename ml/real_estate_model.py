import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

class RealEstateModel:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path, index_col=0) # Set index_col to 0 to avoid using the first column as a feature ("No")
        self.model = None
        self.required_columns = []

    def split_data(self, target_column, test_size=0.2, random_state=42):
        X = self.data.drop(columns=[target_column])
        y = self.data[target_column]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        self.required_columns = X.columns.tolist()  # Store the required columns for later use (input validation)
        
        return X_train, X_test, y_train, y_test
    
    def train_model(self, X_train, y_train):
        # Use a simple linear regression model for this taskk
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)

    def evaluate_model(self, X_test, y_test):
        if self.model is None:
            raise Exception("Please train (train_model) the model before evaluation.")
        score = self.model.score(X_test, y_test)
        print(f"Model R^2 score: {score:.2f}") # check regression score
        return score
    
    def predict(self, X):
        if self.model is None:
            raise Exception("Please train (train_model) the model before making predictions.")
        return self.model.predict(X)
    
    def save_model(self, model_path):
        # Save trained model
        if self.model is None:
            raise Exception("Please train (train_model) the model before saving.")
        
        joblib.dump(self.model, model_path)

    def load_model(self, model_path):
        self.model = joblib.load(model_path)