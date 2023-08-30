
import requests
import urllib.request
import pprint
from geopy.geocoders import Nominatim
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import os
import numpy as np
from django.conf import settings
from geopy.distance import geodesic
import matplotlib.font_manager as fm
from matplotlib import font_manager
import matplotlib
from PIL import Image, ImageDraw, ImageFont



urllib.request.urlretrieve("https://raw.githubusercontent.com/2Moogi/Alice/master/K_A_L_L.csv", filename="kall_data.csv")
kall_df = pd.read_csv("kall_data.csv")

urllib.request.urlretrieve("https://raw.githubusercontent.com/2Moogi/Alice/master/safety_score_21_4.csv", filename="safety_data.csv")

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
                
                #폰트 설정
                matplotlib.font_manager._rebuild()
                font_path = fm.findSystemFonts(fontpaths=None, fontext='ttf')
                nanum_font = [font for font in font_path if 'Nanum' in font]
                font_manager._rebuild()

                if nanum_font:
                    plt.rcParams['font.family'] = 'NanumGothic'
                
                # 그래프 생성
                # 정리된 코드
                
                fig1 = plt.figure(figsize=(5, 5))
                ax1 = fig1.add_subplot(121, projection='3d')

              # 각 항목에 따른 높이를 가져오는 딕셔너리
                height_mapping = {'Red': 25, 'Orange': 45, 'Yellow': 65, 'Green': 85, 'Blue': 105}
                numeric_values = selected_data.iloc[0].apply(lambda x: height_mapping.get(x, 0))
                color_mapping = {'Red': 'red', 'Orange': 'orange', 'Yellow': 'yellow', 'Green': 'green', 'Blue': 'blue'}
                height_mapping_x = {'방범지수': 25, '토지이용지수': 50, '상권지수': 75, '인구지수': 100}

                color_values = selected_data.iloc[0].apply(lambda x: color_mapping.get(x, 'gray'))

                numeric_values_x = selected_data.iloc[0].apply(lambda x: height_mapping_x.get(x, 0))

                x_labels = ['방범지수', '토지이용지수', '상권지수', '인구지수']  # x 축 라벨 리스트

                x_pos = np.arange(len(numeric_values_x[:-1]))
                y_pos = np.zeros(1)
                z_pos = np.zeros(len(numeric_values[:-1]))
                dz = numeric_values[:-1]

            # 원기둥 모양의 3D 막대 그래프 생성
                ax1.bar3d(x_pos, y_pos, z_pos, 0.8, 0.8, dz, shade=True, color=color_values[:-1], alpha=0.7)

            # x 축 라벨 설정
                ax1.set_xticks(x_pos)
                ax1.set_xticklabels(x_labels, rotation=45, ha='right')

              # y 축 눈금과 라벨 비활성화
                ax1.set_yticks([])
                ax1.set_yticklabels([])

              # z 축 눈금 설정
                z_ticks = np.arange(0, 101, 20)  # 0부터 100까지 10 단위로 눈금 생성
                ax1.set_zticks(z_ticks)

                ax1.set_ylabel("")  # y 축 라벨을 빈 문자열로 설정하여 라벨을 제거
                ax1.set_zlabel("높이")
                ax1.set_title("상권 데이터 (3D 원기둥 그래프)")

                
                # 그래프를 이미지 파일로 저장
                fig1.tight_layout()
                file_path1 = os.path.join(settings.BASE_DIR, 'static/graph_output_1.png')
                fig1.savefig(file_path1, bbox_inches='tight')
                plt.close(fig1)

                
                ###########################################################################
                
                fig2 = plt.figure(figsize=(5, 2.3))
                ax2 = fig2.add_subplot(111)
                ax2.axis('off') # 축과 라벨 비활성화

                image = Image.new('RGB', (100, 100), color=color_mapping[selected_data.iloc[0][-1]])

                draw = ImageDraw.Draw(image)
                font = ImageFont.load_default()
                text = selected_data.iloc[0][-1]
                text_width, text_height = draw.textsize(text, font=font)
                text_position = ((100 - text_width) // 2, (100 - text_height) // 2)
                draw.text(text_position, text, fill='white', font=font)

                ax2.imshow(image)

                plt.subplots_adjust(left=0.05, right=0.95, top=0.85, bottom=0.15)
                plt.tight_layout()
                plt.show()
                
                # 그래프를 이미지 파일로 저장
                fig2.tight_layout()
                file_path2 = os.path.join(settings.BASE_DIR, 'static/graph_output_2.png')
                fig2.savefig(file_path2,bbox_inches='tight')
                plt.close(fig2)

                


            else:
                response_data['error'] = "일치하는 데이터가 없습니다."
        else:
            response_data['error'] = "주소를 찾을 수 없습니다."
    else:
        response_data['error'] = f"{search_query}에 대한 검색 결과가 없습니다."
        
    return response_data

if __name__ == "__main__":
    main()