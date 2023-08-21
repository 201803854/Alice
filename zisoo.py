
import requests
import urllib.request
import pprint
from geopy.geocoders import Nominatim
import pandas as pd
import matplotlib.pyplot as plt
import os
from django.conf import settings
from geopy.distance import geodesic


urllib.request.urlretrieve("https://raw.githubusercontent.com/2Moogi/Alice/master/K_A_L_L.csv", filename="kall_data.csv")
kall_df = pd.read_csv("kall_data.csv")

urllib.request.urlretrieve("https://raw.githubusercontent.com/2Moogi/Alice/master/safety_score_21_4.csv", filename="safety_data.csv")
safety_df = pd.read_csv("safety_data.csv")

def kakao_search(query, api_key):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    params = {
        "query": query
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data

def geocoding(address):
    geolocator = Nominatim(user_agent='South Korea', timeout=None)
    location = geolocator.geocode(address)
    if location:
        crd = {"lat": str(location.latitude), "lng": str(location.longitude)}
        return crd
    else:
        return None

def find_nearest_distinct(user_lat, user_lng, df):
    shortest_distance = float('inf')
    nearest_distinct = None
    user_location = (user_lat, user_lng)

    for _, row in df.iterrows():
        distinct_location = (row['위도'], row['경도'])
        distance = geodesic(user_location, distinct_location).kilometers

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_distinct = row

    return nearest_distinct

def main(words_with_label_25):
    plt.close()
    kakao_api_key = "8f969aa6d187fa027d760fa875f9ca19"
    search_query = words_with_label_25  # 첫 번째 단어를 사용
    result = kakao_search(search_query, kakao_api_key)
    response_data = {}

    if result.get('documents'):
        first_result = result['documents'][0]
        address_name = first_result['address_name']
        crd = geocoding(address_name)
        if crd:
            df = kall_df
            nearest_distinct_result = find_nearest_distinct(float(crd['lat']), float(crd['lng']), df)
            keyword = nearest_distinct_result['키워드']
            csv_data = pd.read_csv("safety_data.csv")
            matching_rows = csv_data[csv_data['상권명'] == keyword]

            if not matching_rows.empty:
                required_columns = ['방범지수', '토지이용지수', '상권지수', '인구지수', '안심상권지수']
                selected_data = matching_rows[required_columns]
                response_data['selected_data'] = selected_data.to_dict(orient='records')[0]
                
                # 그래프 생성
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

                color_mapping = {'Red': 'red', 'Orange': 'orange', 'Yellow': 'yellow', 'Green': 'green', 'Blue': 'blue'}
                height_mapping = {'Red': 20, 'Orange': 40, 'Yellow': 60, 'Green': 80, 'Blue': 100}

                numeric_values = selected_data.iloc[0].apply(lambda x: height_mapping.get(x, 0))
                color_values = selected_data.iloc[0].apply(lambda x: color_mapping.get(x, 'gray'))

                ax1.bar(numeric_values.index[:-1], numeric_values[:-1], color=color_values[:-1], alpha=0.7)
                ax1.set_xticks(numeric_values.index[:-1])
                ax1.set_xticklabels(selected_data.columns[:-1], rotation=0)
                ax1.set_yticks([0, 20, 40, 60, 80])
                ax1.set_yticklabels([0, 20, 40, 60, 80])
                ax1.set_ylabel("값")
                ax1.set_title("상권 데이터 (지수 그래프)")

                ax2.bar(numeric_values.index[-1], height_mapping[selected_data.iloc[0][-1]], color=color_mapping[selected_data.iloc[0][-1]], alpha=0.7, width=0.5)
                ax2.set_xticks(numeric_values.index[-1])
                ax2.set_xticklabels([selected_data.columns[-1]])
                ax2.set_yticks([20, 40, 60, 80, 100])
                ax2.set_yticklabels([20, 40, 60, 80, 100])
                ax2.set_ylabel("값")
                ax2.set_title("안심상권지수 그래프")

                # 그래프를 이미지 파일로 저장
                file_path = os.path.join(settings.BASE_DIR, 'static/graph_output.png')
                fig.savefig(file_path)
                plt.close()


            else:
                response_data['error'] = "일치하는 데이터가 없습니다."
        else:
            response_data['error'] = "주소를 찾을 수 없습니다."
    else:
        response_data['error'] = f"{search_query}에 대한 검색 결과가 없습니다."
        
    return response_data

if __name__ == "__main__":
    main()