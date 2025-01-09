from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import joblib
from newspaper import Article
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load models and vectorizer
try:
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    log_reg_model = joblib.load("log_reg_model.pkl")
    gb_model = joblib.load("gb_model.pkl")
    rf_model = joblib.load("rf_model.pkl")
    nb_model = joblib.load("nb_model.pkl")
except Exception as e:
    raise Exception(f"Failed to load models or vectorizer: {str(e)}")

# Model accuracies (weights)
model_accuracies = [0.9717, 0.9811, 0.9780, 0.9230]

# Normalize weights
normalized_weights = np.array(model_accuracies) / sum(model_accuracies)

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

@app.route("/prediction", methods=["POST"])
def predict():
    try:
        # Identify if the request is from Chrome extension
        source = request.headers.get("X-Source", "unknown")
        if source == "chrome-extension":
            print("Received request from Chrome extension.")
        # Extract URL from JSON body (for AJAX)
        data = request.get_json()
        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "Please provide a valid URL."}), 400

        # Extract and preprocess text from URL
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text.strip()
            if not text:
                raise ValueError("The article contains no text.")
        except Exception as e:
            return jsonify({"error": f"Failed to extract article text: {str(e)}"}), 400

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
        confidence = round(weighted_avg_prob * 100, 2)  # Confidence percentage
        final_prediction = "Real" if weighted_avg_prob > 0.5 else "Fake"

        # Return the prediction results
        return jsonify({
            "prediction": final_prediction,
            "confidence_score": confidence,
            "model_scores": {
                "Logistic Regression": round(model_probabilities[0] * 100, 2),
                "Gradient Boosting": round(model_probabilities[1] * 100, 2),
                "Random Forest": round(model_probabilities[2] * 100, 2),
                "Naive Bayes": round(model_probabilities[3] * 100, 2),
            }
        })

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)