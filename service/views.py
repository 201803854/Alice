




from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import ner
import re


API_URL = "https://api-inference.huggingface.co/models/kyungmin011029/test_fith"
HEADERS = {"Authorization": "Bearer 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"}


@csrf_exempt
def convert_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_data = request.FILES['audio'].read()
        response = query_hugging_face_model(audio_data)
        print("Response Content:", response)
        result_text = response['text']
        ner_result = ner.ner_prediction(result_text)
        words_with_label_25 = [word for word, label in ner_result if label == 'LABEL_25']
        print(words_with_label_25)
        response['words_with_label_25'] = words_with_label_25
    
        return JsonResponse(response)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def query_hugging_face_model(audio_data):
    response = requests.post(API_URL, headers=HEADERS, data=audio_data)
    return response.json()

