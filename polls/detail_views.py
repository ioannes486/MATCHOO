# from django.shortcuts import render

# def result(request):
#     return render(request, 'result.html')

# def store_detail(request):
#     return render(request, 'store_detail.html')

# def my_view(request):
#     # 크롤링한 결과를 가져오는 코드
#     crawling_review = # 크롤링 결과로 생성된 df에서 review column 가져오기
#     crawling_bert = # 크롤링 결과로 생성된 df에서 bert column 가져오기
#     # 특정 조건에 해당하는 데이터만 추출
#     filtered_review = [data for data in crawling_review if data['매장 명과 동일한 행 조건 걸어주기']]
#     filtered_bert = [data for data in crawling_bert if data['매장 명과 동일한 행 조건 걸어주기']]

#     # 새로운 HTML 템플릿에 전달하기 위해 context에 데이터를 추가
#     context = {'filtered_review': filtered_review,
#                'filtered_bert': filtered_bert,}

#     # render() 함수를 사용하여 새로운 HTML 템플릿을 렌더링하고 반환
#     return render(request, 'store_detail.html', context)