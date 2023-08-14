import requests

API_URL = "https://api-inference.huggingface.co/models/kyungmin011029/test_fith"
headers = {"Authorization": "Bearer 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"}


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()


output = query("KsponSpeech_E06000.wav")

