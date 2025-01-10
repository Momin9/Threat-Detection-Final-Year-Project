import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib

# Load large dataset
df = pd.read_csv('enhanced_dataset.csv')

# Feature extraction
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['request_data'])
y = df['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = MultinomialNB()
model.fit(X_train, y_train)

# Save model and vectorizer
joblib.dump(model, 'train.h5')
joblib.dump(vectorizer, 'vectorizer.pkl')

print("Robust model trained and saved with large dataset!")
