import numpy as np

def check_fake_news_weighted(text, vectorizer, models, model_accuracies):
    """
    Determines if a news article is fake or real based on weighted model predictions.

    Parameters:
        text (str): The input text to evaluate.
        vectorizer (TfidfVectorizer): The vectorizer for transforming text into features.
        models (dict): A dictionary of trained models.
        model_accuracies (list): The accuracies of each model for weighted prediction.

    Returns:
        tuple: Final prediction ('Real' or 'Fake'), weighted average probability, and individual model probabilities.
    """
    # Vectorize the text
    text_vectorized = vectorizer.transform([text])

    # Get probabilities for each model
    model_probabilities = [model.predict_proba(text_vectorized)[0][1] for model in models.values()]

    # Calculate weighted average of probabilities
    weighted_avg_prob = sum(prob * weight for prob, weight in zip(model_probabilities, model_accuracies))
    final_prediction = "Real" if weighted_avg_prob > 0.5 else "Fake"

    return final_prediction, weighted_avg_prob, model_probabilities
