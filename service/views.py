
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import requests
import ner

import zisoo

from kss import split_sentences

# whisper fine-tuned model api
API_URL = "https://api-inference.huggingface.co/models/kyungmin011029/test_seven"
#code-classification model api
API_URL2 = "https://api-inference.huggingface.co/models/kyungmin011029/code_alice"
#code_category model api
API_URL3 = "https://api-inference.huggingface.co/models/kyungmin011029/category_alice"
HEADERS = {"Authorization": "Bearer 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"}

# csrf exempt
@csrf_exempt
# convert audio to text, ner, code classfication
def convert_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_data = request.FILES['audio'].read()
        response = query_hugging_face_model(audio_data)
        print('\n들어온 음성: ', response)
        sentences = split_sentences(response['text'])
        print("\n분리된 문장:", sentences)
        results=[]
        for sentence in sentences:
            temp = {'text' : sentence}
            code_class = query(sentence)
            print(code_class)
            if code_class:
                results.append([code_class[0][0].get('label')[-1],code_class[0][0].get('score'),temp])
            else:
                continue
        results = sorted(results, key = lambda x : (x[0], -x[1]))
        print("\n문장 별 가장 높은 코드: ", results)
        urgent_code = results[0]
        print("\n긴급코드: ", urgent_code)
        category_sentence=urgent_code[2]
        category = query_category(category_sentence)
        print(category)
        code_classifiering= code_classifier(urgent_code, category)
        result_text = response['text']

        # call ner.py for ner / result_text<->
        ner_result = ner.ner_prediction(result_text)
        words_with_label_25 = [word for word, label in ner_result if label == 'LABEL_25' and word != '[CLS]' and word!= '[SEP]']
        print('\nNER 라벨: ', words_with_label_25)

        zisoo_result = zisoo.main(words_with_label_25)
        response.update(zisoo_result)
        print('\n지수 결과' ,zisoo_result) 

        response['words_with_label_25'] = words_with_label_25
        response['code'] = code_classifiering
        print("Response Content:", response)
        return JsonResponse(response)


    return JsonResponse({'error': 'Invalid request'}, status=400)

# call stt model


def query_hugging_face_model(audio_data):
    response = requests.post(API_URL, headers=HEADERS, data=audio_data)
    return response.json()
# call code_classfication model


def query(payload):
    response = requests.post(API_URL2, headers=HEADERS, json=payload)
    return response.json()


#call code_category model

def query_category(text):
    response = requests.post(API_URL3, headers=HEADERS, json=text)
    return response.json()

def code_classifier(code, category):
    # if type(code) == 'int' or type(code) == 'str': count = code 
    result = "CODE"+str(code[0])
    category = category[0]
    print(category)
  #result[0]['score']
    max_prob = code[1]
    max_prob *= 100
    count = result
    category_prob = category['score']
    check = category['label']
    check = check.replace('LABEL_', '')
    check = int(check)
    
    mapping_ = {'가정폭력':0, '일반절도':1, '살인':2, '성매매/알선':3, '과도노출':4, '무허가주류/담배':5, '무전취식': 6, '보이스피싱':7, '손괴': 8, '강제추행/강간': 9, '범행예고': 10, '시비난동행패소란':11, '일반소음': 12, '적재물낙하': 13, '주취자보호': 14, '미귀가자': 15, '교통서비스': 16, '층간소음': 17, '화재': 18, '가출/실종': 19, '도박': 20, '미성년자고용/출입': 21, '보이스피싱': 22, '공사장소음': 23, '강력 일반폭력': 24, '일반폭력': 25, '분실물신고': 26, '습득신고': 27, '길안내': 28, '전기누전': 29, '수도관파열': 30, '불법주정차': 31, '시설민원': 32, '쓰레기무단투기': 33, '교통사고': 34, '유기': 35, '다중밀집': 36, '일상대화': 37}
    # mapping_ = {'강력 일반폭력':0, '가정폭력':1, '살인': 2, '유기': 3, '변사' : 4, '총성/폭발음' : 5, '교통사고': 6, '납치': 7, '방화': 8, '일반폭력':9, '일반절도':10, '층간소음':11, '화재':12, '가출/실종': 13, '도박':14, '성매매/알선': 15, '과도노출': 16, '무허가주류/담배': 17, '무전취식':18, '보이스피싱': 19, '손괴': 20, '강제추행/강간': 21, '범행예고': 22, '시비난동행패소란': 23, '일반소음': 24, '적재물낙하': 25, '주취자보호': 26, '미귀가자': 27, '교통서비스': 28, '도박': 29, '미성년자고용/출입': 30, '공사장소음': 31, '분실물신고': 32, '습득신고': 33, '길안내': 34, '동물사체처리': 35, '전기누전' : 36, '수도관파열': 37, '불법주정차' : 38, '시설민원' : 39, '불법부착물': 40, '동물관련민원': 41, '면허증민원': 42, '금융범죄의심': 43, '불법번호판민원': 44, '공사장안전민원': 45, '쓰레기무단투기': 46, '수해위험': 47, '붕괴위험': 48, '다중밀집' : 49, '주거침입' : 50, '일상대화': 51}  # mapping_ = {'강력 일반폭력':0, '가정폭력':1, '일반폭력':2, '일반절도':3, '층간소음':4, '화재':5, '가출/실종': 6, '도박':7, '성매매/알선': 8, '과도노출': 9, '무허가주류/담배': 10, '무전취식':11, '보이스피싱': 12, '손괴': 13, '강제추행/강간': 14, '범행예고': 15, '시비난동행패소란': 16, '일반소음': 17, '적재물낙하': 18, '주취자보호': 19, '미귀가자': 20, '교통서비스': 21, '도박': 22, '미성년자고용/출입': 23, '공사장소음': 24, '분실물신고': 25, '습득신고': 26, '길안내': 27, '동물사체처리': 28, '전기누전' : 29, '수도관파열': 30, '불법주정차' : 31, '시설민원' : 32, '불법부착물': 33, '동물관련민원': 34, '면허증민원': 35, '금융범죄의심': 36, '불법번호판민원': 37, '공사장안전민원': 38, '쓰레기무단투기': 39 }
    # mapping_ = {'가정폭력':0, '일반절도':1, '도박':2, '성매매/알선':3, '과도노출':4, '무허가주류/담배':5, '무전취식': 6, '보이스피싱':7, '손괴': 8, '강제추행/강간': 9, '범행예고': 10, '시비난동행패소란':11, '일반소음': 12, '적재물낙하': 13, '주취자보호': 14, '미귀가자': 15, '교통서비스': 16, '층간소음': 17, '화재': 18, '가출/실종': 19, '도박': 20, '미성년자고용/출입': 21, '보이스피싱': 22, '공사장소음': 23, '강력 일반폭력': 24, '일반폭력': 25}
    map = {v:k for k,v in mapping_.items()}
    get = map.get(check)
    
    # 수정
    if get =='일상대화': count = '미분류'
    code_zip = {'count': count, 'prob': str(round(max_prob, 2))+"%", 'get': get}

    return code_zip

