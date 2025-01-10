import joblib

# Load the trained model and vectorizer
MODEL = joblib.load('threat_app/train.h5')
VECTORIZER = joblib.load('threat_app/vectorizer.pkl')

def detect_threat(request_data):
    vectorized_data = VECTORIZER.transform([request_data])
    prediction = MODEL.predict(vectorized_data)
    return prediction[0] == 1  # True if threat detected
