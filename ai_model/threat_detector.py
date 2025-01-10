from ai_model.train_model import ThreatDetectionModel
import os

class ThreatDetector:
    def __init__(self):
        self.model = ThreatDetectionModel()
        data_path = os.path.join(os.path.dirname(__file__), "synthetic_dataset.csv")
        if not os.path.exists(self.model.model_path):
            self.model.train_model(data_path)

    def is_threat(self, request_data):
        try:
            # Example: Extract features (adjust parsing for real requests)
            features = [float(value) for value in request_data.split(",")]
            is_threat = self.model.predict(features)

            # If new threat type detected, update the model
            if is_threat == 1:
                print("Threat Detected. Updating Model.")
                self.model.update_model(features, label=1)
            return is_threat
        except Exception as e:
            print(f"Error in threat detection: {e}")
            return 0  # Default to "not a threat"

if __name__ == "__main__":
    # Example: Manual test for threat detection
    detector = ThreatDetector()
    sample_request = "0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0"
    print(f"Is Threat: {detector.is_threat(sample_request)}")
