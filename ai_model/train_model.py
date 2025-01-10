import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn.semi_supervised import SelfTrainingClassifier

class ThreatDetectionModel:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), "threat_detection_model.pkl")

    def pre_train_unsupervised(self, X):
        """Unsupervised learning for feature clustering."""
        kmeans = KMeans(n_clusters=2, n_init=10, random_state=42)
        cluster_labels = kmeans.fit_predict(X)
        return cluster_labels

    def train_model(self, data_path):
        # Load dataset
        df = pd.read_csv(data_path)
        X = df.drop("threat", axis=1).values
        y = df["threat"].values

        # Unsupervised Pre-Training
        cluster_labels = self.pre_train_unsupervised(X)
        print("Clustering complete. Unsupervised labels generated.")

        # Split into train and test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Mask labels for semi-supervised learning
        mask = np.random.rand(len(y_train)) < 0.7
        y_train_semi_supervised = np.where(mask, -1, y_train)

        # Train with Semi-Supervised Learning
        base_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model = SelfTrainingClassifier(base_model)
        self.model.fit(X_train, y_train_semi_supervised)

        # Evaluate model
        predictions = self.model.predict(X_test)
        acc = accuracy_score(y_test, predictions)
        print(f"Model Accuracy: {acc * 100:.2f}%")

        # Save the model
        joblib.dump(self.model, self.model_path)
        print(f"Model trained and saved to {self.model_path}")

    def predict(self, features):
        if self.model is None:
            self.model = joblib.load(self.model_path)
        return self.model.predict([features])[0]

    def update_model(self, features, label):
        """Reinforcement learning - update model with new data."""
        X = np.array(features).reshape(1, -1)
        y = np.array([label])
        self.model.fit(X, y)
        joblib.dump(self.model, self.model_path)
        print("Model updated with new threat information.")

if __name__ == "__main__":
    # Example: Manual training
    model = ThreatDetectionModel()
    data_path = os.path.join(os.path.dirname(__file__), "synthetic_dataset.csv")
    model.train_model(data_path)
