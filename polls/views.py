from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
import json
import openai
from ._crawling import crawl_reviews, to_df
from django.conf import settings

def index(request):
    context = {"title": 'Home'}
    print(request)

    return render(request, "polls/index.html", context)
    

    
def detail(request):
    return render(request, "polls/detail.html", {"title": 'question'})

# 이거 꼭 바꿔라!!!!!!!!!!!!! 안바꾸면 3대멸망 아래로 3대임 내 대는 아님
openai.api_key = settings.OPENAI_API_KEY

def results(request):


    if request.method == 'POST':
        # 요청 받아서 문구 만들기
        res = request.POST
        user_message = '앞으로 단답으로만 대답해 나는 {}고 {}고 {}고 {}고 {}고 {}해 나한테 부연설명,부가설명없이 단답형으로 한국 여행지 한 곳 무조건 이름만 추가설명없이 나오게 해줘'.format(res.get('trip'), res.get('type'), res.get('movement'), res.get('pop'), res.get('with'), res.get('how'), )

        # 만든 문구로 챗봇에게 넘겨주기
        messages = [{'role': 'user', 'text': user_message}]
        completion = openai.Completion.create(
            model='text-davinci-003',
            prompt='\n'.join([f'{m["role"]}: {m["text"]}' for m in messages]),
            temperature=1, 
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=15,
        )
        assistant_message = completion.choices[0].text.strip()
        messages.append({'role': 'assistant', 'text': assistant_message})

        # 추천한 여행지와 "맛집" 키워드를 함께 검색하여 크롤링
        destination = assistant_message
        keyword = '맛집'
        crawl_reviews(f"{destination} {keyword}")
        store_list = list(set(to_df().store.to_list()))

        context = {'bot_message': assistant_message, 
                   'store_list' : store_list}

        return render(request, 'polls/results.html', context)
def vote(request):
    pass

