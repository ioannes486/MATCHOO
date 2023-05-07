from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.views.decorators.cache import cache_page
import json
import openai
from ._crawling import crawl_reviews, to_df
from ._chat import recommand_traveling_site
from django.conf import settings
import pandas as pd
import time

from .models import Review

def index(request):
    context = {"title": 'Home'}
    print(request)

    return render(request, "polls/index.html", context)
    

    
def detail(request):
    return render(request, "polls/detail.html", {"title": 'question'})

# 이거 꼭 바꿔라!!!!!!!!!!!!! 안바꾸면 3대멸망 아래로 3대임 내 대는 아님
openai.api_key = settings.OPENAI_API_KEY
openai.api_key = settings.OPENAI_API_KEY



def results(request):



    if request.method == 'POST':
        global df
        # 요청 받아서 문구 만들기
        res = request.POST
        bot_message = recommand_traveling_site(res)
        #store_list = to_df().prediction
        

        # 추천한 여행지와 "맛집" 키워드를 함께 검색하여 크롤링
        keyword = '맛집'
        query = f"{bot_message} {keyword}"
        crawl_reviews(query)
        df = to_df()

        df_html = df.to_html(
                        columns=['store', 'review'],
                        index=False, na_rep="", bold_rows=True,
                        classes=["table", "table-hover", "table-processed"])
        
        store_list = to_df().store.unique().tolist()
        

        context = {
            'bot_message': bot_message, 
            'store_list' : store_list,
            'df_html' : df_html,}
        

        return render(request, 'polls/results.html', context)
    
    else:
        return render(request, 'loading.html')



def store_detail(request):

    store = request.GET.get('store')
    reviews = Review.objects.filter(store=store)

    # 가게 이름 가져오기
    store_name = df[df['store']==store]['store'].iloc[0]

    context = {
        'store': store_name,
        'reviews': reviews,
    }

    return render(request, 'polls/store_detail.html', context)


def give_survey(request):
    return render(request, 'give_survey.html')

