import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib
import os

def train_baseline():
    print("🚀 Starting Baseline Model Training...")
    
    # Mock Data for demonstration
    data = {
        'text': ["This is a fake news article"] * 50 + ["Verified real news content"] * 50,
        'label': [1] * 50 + [0] * 50
    }
    df = pd.DataFrame(data)
    
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2)
    
    # Pipeline
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    
    model = LogisticRegression()
    model.fit(X_train_vec, y_train)
    
    # Save
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/baseline_model.pkl")
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    print("✅ Model saved to models/")

if __name__ == "__main__":
    train_baseline()
