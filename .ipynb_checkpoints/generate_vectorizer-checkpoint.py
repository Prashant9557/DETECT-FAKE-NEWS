from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Sample data to train the vectorizer
sample_data = ["Fake news example", "Real news example"]

# Initialize and train the vectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(sample_data)

# Save the trained vectorizer
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("Vectorizer has been saved as 'tfidf_vectorizer.pkl'.")


