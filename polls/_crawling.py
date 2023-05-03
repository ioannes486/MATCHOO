import requests 
from selenium.webdriver.common.by import By
import pandas as pd
import json
import time
from django.conf import settings

from ._preprocess import driver, get_reviews, get_stars, append_to_list, unfold
def crawl_reviews(query, size=10):
    # 1. 링크 크롤링
    ## 변수 초기화
    url_place = {}
    all_dict = {}
    one_dict = {'별점':[], '메뉴':[], '리뷰':[]}

    ## API 요청 URL 설정
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"

    ## API 요청 헤더정보와 파라미터 설정
    headers = {"Authorization": f"KakaoAK {settings.KAKAO_API_KEY}"}
    params = {"query": query,"size": size}

    ## API 요청 및 결과 받아오기
    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()

    ## {'상호명' : 'url'} 형태의 딕셔너리로 만들기
    for i in range(len(json_data['documents'])):
        key = json_data['documents'][i]['place_name'] # 가게 이름을 key로
        url_place[key] = json_data['documents'][i]['place_url'] # 가게의 주소 value로 저장

    #2. 리뷰크롤링
    for idx, key in enumerate(url_place):

        review_all = []
        star_all = []
        
        driver.get(url_place[key]) # url[key] -> 가게의 카카오맵 주소
        
        time.sleep(3)
        
        # unfold -> 페이지의 더보기 버튼 모두 찾아서 누르기 -> 추가 메뉴 확인 및 리뷰 글 전체 확인
        unfold('btn_fold')    


        try:
            # 리뷰 페이지 전체를 감싸는 엘리먼트 가져오기
            review_wrap = driver.find_element(By.CSS_SELECTOR, 'div.evaluation_review')
            while True:
                # 현재 페이지에서 리뷰 가져오기
                review_all = append_to_list(review_all, get_reviews('comment_info'))
                star_all = append_to_list(star_all, get_stars('num_rate'))

                # 다음 버튼이 없을 경우 더 이상 가져올 리뷰가 없음
                if 'disabled' in review_wrap.find_element(By.CSS_SELECTOR, 'a.btn_g.btn_page.next').get_attribute('class'):
                    break

                # 다음 페이지로 이동
                driver.find_element(By.CSS_SELECTOR, 'a.btn_g.btn_page.next').click()
                time.sleep(3)

                # 더보기 버튼 누르기
                unfold('btn_fold')

                # 리뷰 페이지 전체를 감싸는 엘리먼트 다시 가져오기
                review_wrap = driver.find_element(By.CSS_SELECTOR, 'div.evaluation_review')
        except:
            print(idx, '에러가 났다')
            review_all = append_to_list(review_all, get_reviews('comment_info'))

        # 한 가게의 모든 리뷰를 딕셔너리에 추가
        one_dict = {'reviews':review_all}
        all_dict[key] = one_dict

        
    time.sleep(1)

    path = "./down_3.0_data.json"

    #3. 파일을 json형태로 저장
    with open(path, 'w', encoding='UTF-8') as outfile:
        json.dump(all_dict, outfile, indent=4,ensure_ascii=False)
        
    time.sleep(1)

    driver.quit()

    return all_dict

def to_df(path='./down_3.0_data.json'):
    with open(path, 'r',encoding="UTF-8") as f:
        json_data = json.load(f)
    
    review_data = []
    name_data = []

    for store in json_data:
        for j in range(len(json_data[store]['reviews'])):
            name_data.append(store)
            review_data.append(json_data[store]['reviews'][j])

    df = pd.DataFrame({'store' :name_data, 'review': review_data})
    return df


if __name__ == '__main__':
    print(crawl_reviews('강남맛집'))
    print(to_df())
    #crawl_reviews('강남맛집')

# 후속과제 : 리뷰가 없거나 짧을 경우 크롤링 하지 않게 만들기, 리뷰 개수 늘리기