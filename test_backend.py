import requests

url = "http://127.0.0.1:5000/predict"
article_url = "https://www.newindianexpress.com/thesundaystandard/2024/Nov/24/future-tense-for-sharad-pawar-uddhav-thackeray"  # Replace with a valid article URL

try:
    response = requests.post(url, json={"url": article_url})  # Ensure the key is "url"
    if response.status_code == 200:
        print("Response from the server:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"An error occurred: {e}")
