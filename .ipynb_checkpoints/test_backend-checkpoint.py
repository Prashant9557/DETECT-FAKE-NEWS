import requests
import json

def test_prediction(article_url):
    print(f"Testing URL: {article_url}")
    url = "http://127.0.0.1:5000/predict"
    
    try:
        # First check if the server is running
        health_check = requests.get("http://127.0.0.1:5000/")
        if health_check.status_code != 200:
            print("Server is not running properly")
            return

        # Prepare the request
        headers = {'Content-Type': 'application/json'}
        data = {'url': article_url}
        
        # Make the request
        print("Sending request to server...")
        response = requests.post(url, json=data, headers=headers)
        
        # Pretty print the response
        print("\nResponse Status Code:", response.status_code)
        
        if response.status_code == 200:
            result = response.json()
            print("\nPrediction Results:")
            print("-" * 50)
            print(f"Article URL: {result['url']}")
            print(f"Final Prediction: {result['prediction']}")
            print(f"Confidence Score: {result['confidence_score']:.2f}%")
            print("\nIndividual Model Predictions:")
            for model, pred in result['model_predictions'].items():
                print(f"{model}: {pred}")
        else:
            print("Error Response:")
            try:
                error_msg = response.json()
                print(json.dumps(error_msg, indent=2))
            except:
                print(response.text)
                
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure backend.py is running!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Test with a news article URL
    test_urls = [
        "https://www.reuters.com/world/us/biden-takes-thanksgiving-break-nantucket-2023-11-21/",
        "https://www.bbc.com/news/world-middle-east-67511135"
    ]
    
    for article_url in test_urls:
        print("\nTesting new article...")
        print("=" * 70)
        test_prediction(article_url)
        print("=" * 70)