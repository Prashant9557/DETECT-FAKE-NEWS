from flask import Flask, request, jsonify, render_template
import joblib
from newspaper import Article
import numpy as np


# Load models and vectorizer
try:
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    log_reg_model = joblib.load("logistic_regression_model.pkl")
    gb_model = joblib.load("gradient_boosting_model.pkl")
    rf_model = joblib.load("random_forest_model.pkl")
    nb_model = joblib.load("naive_bayes_model.pkl")
except Exception as e:
    raise Exception(f"Failed to load models or vectorizer: {str(e)}")

# Model accuracies (weights)
model_accuracies = [0.9717, 0.9811, 0.9780, 0.9230]

# Normalize weights
normalized_weights = np.array(model_accuracies) / sum(model_accuracies)

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Validate input
        data = request.json
        if not data or "url" not in data:
            return jsonify({"error": "Invalid input. Please provide a JSON payload with a 'url' key."}), 400
        
        url = data.get("url")

        # Extract and preprocess text from URL
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text.strip()
            if not text:
                raise ValueError("Article text is empty.")
        except Exception as e:
            return jsonify({"error": f"Failed to extract article text: {str(e)}"}), 500

        # Vectorize the text
        text_vectorized = vectorizer.transform([text])

        # Perform predictions using all models with probabilities
        models = {
            "Logistic Regression": log_reg_model,
            "Gradient Boosting": gb_model,
            "Random Forest": rf_model,
            "Naive Bayes": nb_model
        }

        # Get probabilities for each model
        model_probabilities = [model.predict_proba(text_vectorized)[0][1] for model in models.values()]

        # Calculate weighted average of probabilities
        weighted_avg_prob = sum(prob * weight for prob, weight in zip(model_probabilities, normalized_weights))
        confidence = weighted_avg_prob  # Confidence score for the prediction
        final_prediction = "Real" if weighted_avg_prob > 0.5 else "Fake"

        return jsonify({
            "url": url,
            "prediction": final_prediction,
            "confidence_score": round(confidence * 100, 2),  # Confidence percentage
            "model_predictions": {
                model_name: round(prob, 4) for model_name, prob in zip(models.keys(), model_probabilities)
            }
        })
    
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
