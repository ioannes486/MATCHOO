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
    
    if 'json_data' in locals() and 'documents' in json_data:
        for i in range(len(json_data['documents'])):
            key = json_data['documents'][i]['place_name'] # 가게 이름을 key로
            url_place[key] = json_data['documents'][i]['place_url'] # 가게의 주소 value로 저장
    else:
    # 예외 처리 코드 추가
        pass # 예외 처리 코드를 추가하세요.

    #2. 리뷰크롤링
    for idx, key in enumerate(url_place):

        review_all = []
        star_all = []
        
        driver.get(url_place[key]) # url[key] -> 가게의 카카오맵 주소
        
        time.sleep(3)
        
        # unfold -> 페이지의 더보기 버튼 모두 찾아서 누르기 -> 추가 메뉴 확인 및 리뷰 글 전체 확인
        unfold('btn_fold')    


        try:
            page = driver.find_element(By.CLASS_NAME,'wrap_mapdetail lbar_on') # 이 클래스 이름이 바뀐거 같음
            print(page)
            end_page = len(page.text.replace(" ","")) # 페이지를 넘기기
            print(end_page)
            for p in range(2, 11): # 2에서 10까지의 페이지에서 리뷰 가져오기
                                # 얘가 리뷰 가지고 오는 횟수를 정하는거 같은데 어떻게 바꿀까
                
                time.sleep()
                review_all = append_to_list(review_all, get_reviews('comment_info'))
                star_all = append_to_list(star_all, get_stars('num_rate'))
                if (end_page == 2):
                    page_select = "#mArticle > div.cont_evaluation > div.evaluation_review > div > a"

                else:
                    page_select = "#mArticle > div.cont_evaluation > div.evaluation_review > div > a:nth-child("+str(p+1)+")"

                    
                next_page = driver.find_element(By.CSS_SELECTOR,page_select)
                time.sleep(3)
                next_page.click()
                time.sleep(2)
                unfold('btn_fold')
                p+=1

                
        except:
            print(idx, '크롤링 완료')
            review_all = append_to_list(review_all, get_reviews('comment_info'))

            
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