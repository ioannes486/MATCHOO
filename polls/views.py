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

def vote(request):
    pass



def store_detail(request):

# 3안
    for index, row in df.iterrows():
        store = row['store']
        review = row['review']
        prediction = row['prediction']

        review_obj = Review(store=store, review=review, prediction=prediction)
        review_obj.save()

    store = request.GET.get('store')
    reviews = Review.objects.filter(store=store)
    reviews_list = [review.review for review in reviews]
    

    context = {
        'reviews': reviews,
               }

    return render(request, 'polls/store_detail.html', context)


# 2안
    # store_list = request.GET.get('store', '')
    # reviews = Review.objects.filter(store=store_list)
    # context = {'reviews': reviews}
    # return render(request, 'polls/store_detail.html', context)

# 1안
    # grouped = to_df().groupby('store')
    # grouped_review = []
    # for group in grouped:
    #     grouped_review = group[1]['review']
    
    # context = {'grouped_review':grouped_review}

    # return render(request, 'polls/store_detail.html', context)







#     # <label for='activity'> 평소 활동적인걸 좋아하시나요 ? </label>
#     # <input type='radio' id='activity' name='activity' value='yes' />좋아한다
#     # <input type='radio' id='activity' name='activity' value='no' />좋아하지 않는다

#     # # request['activity'] -> "yes" or "no"
#     # if request['activity'] == 'yes':
#     #     prompt += '나는 활동적인 것을 좋아해'
#     # elif request['activity'] == 'no':
#     #     prompt += '나는 활동적인 것을 좋아하지 않아'



#     question = get_object_or_404(Question, pk=question_id)
#     response = request.POST["choice"].split()
#     primary_key = int(response[0])
#     choice = response[1]

#     try:
#         selected_choice = question.choice_set.get(pk=primary_key)
#     except (KeyError, Choice.DoesNotExist):
#         context = {
#             'question' : question,
#             "error_message": "You didn't select a choice.",
#         }
#         return render(request, "polls/detail.html", context)
#     else:
#         selected_choice.votes +=1
#         selected_choice.save()
#         primary_key+=1
#         context = {
#             'primary_key' : primary_key,
#         }
#         #return redirect(f"polls/{primary_key}")wodjns
#         return HttpResponse(reverse(f"polls:detail", args=(primary_key,)))

# def index(request):
#     context = {'title': 'Home'}
#     return render(request, 'polls/index.html', context)

# def detail(request):
#     context = {'title': 'choice'}
#     return render(request, 'polls/detail.html', context)

# def results(request):
#     result = list(request.POST.values())[1:]
#     context = {'title': 'result and info', 'result': result}
#     return render(request, 'polls/results.html', context)
