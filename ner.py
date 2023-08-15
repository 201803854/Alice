from transformers import AutoModelForTokenClassification, AutoTokenizer
import torch

API_URL = "https://api-inference.huggingface.co/models/2Moogi/first_model"
API_TOKEN = {"Authorization": "Bearer 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"}

MODEL_NAME = "2Moogi/first_model"
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME, from_tf=True)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def ner_prediction(sentence):
    # 토크나이징
    tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(sentence)))
    inputs = tokenizer.encode(sentence, return_tensors="pt", add_special_tokens=True)  # add_special_tokens=True

    # 모델 예측
    outputs = model(inputs).logits
    predictions = torch.argmax(outputs, dim=2).squeeze().tolist()  # 결과 형태를 간소화

    # 결과 해석
    id2label = model.config.id2label  # 정확한 라벨 매핑
    labeled_tokens = [(token, id2label[label_id]) for token, label_id in zip(tokens, predictions)]

    # 원하는 형식으로 결과를 조립
    merged_results = []
    temp_token = ""
    temp_label = ""
    for token, label in labeled_tokens:
        if token.startswith("##"):
            temp_token += token[2:]
        else:
            if temp_token:
                merged_results.append((temp_token, temp_label))
                temp_token = ""
            temp_token = token
            temp_label = label
    if temp_token:
        merged_results.append((temp_token, temp_label))

    return merged_results

# ... (나머지 코드는 동일)
if __name__ == "__main__":
    while True:
        sen = input('문장을 입력하세요: ')

        if sen.strip() == '끝':
            break
        else:
            result = ner_prediction(sen)
            print('결과:')
            print(result)
            print()