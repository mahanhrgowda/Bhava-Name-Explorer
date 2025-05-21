# 📁 bhava_poem_app/ml_model/train_guesser.py – Train ML Bhāva classifier

import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from pathlib import Path

# Load expanded dataset
DATA_PATH = Path("assets/full_bhava_dataset.csv")
df = pd.read_csv(DATA_PATH)

# Input & label
X = df["phoneme"]
y = df["bhava"]

# Char-level n-gram vectorization
vectorizer = CountVectorizer(analyzer="char", ngram_range=(1, 3))
X_vec = vectorizer.fit_transform(X)

# Train model
model = MultinomialNB()
model.fit(X_vec, y)

# Save model + vectorizer
Path("ml_model").mkdir(exist_ok=True)
joblib.dump(vectorizer, "ml_model/vectorizer.pkl")
joblib.dump(model, "ml_model/bhava_classifier.pkl")

print("✅ Model trained and saved: bhava_classifier.pkl")
