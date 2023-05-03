from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
import json
import openai
from ._crawling import crawl_reviews, to_df
from django.conf import settings
import pandas as pd

from .models import Review

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
        user_message = '나는 {}고 {}고 {}고 {}고 {}고 {}해 나한테 부연설명 없이 단답형으로 한국여행지 한 곳을 추천해줘'.format(res.get('trip'), res.get('type'), res.get('movement'), res.get('pop'), res.get('with'), res.get('how'), )

        # 만든 문구로 챗봇에게 넘겨주기
        messages = [{'role': 'user', 'text': user_message}]
        completion = openai.Completion.create(
            model='text-davinci-003',
            prompt='\n'.join([f'{m["role"]}: {m["text"]}' for m in messages]),
            temperature=0, # 얼마나 자연스럽게 답을 줄건지에 대해 높을수록 자연스러운 대화 가능
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=15,
        )
        assistant_message = completion.choices[0].text.strip()
        messages.append({'role': 'assistant', 'text': assistant_message})
        bot_message = messages[1]['text'].strip('!')
        bot_message = '강남맛집'
        crawl_reviews(bot_message)
        store_list = list(set(to_df().store.to_list()))


        context = {'bot_message': bot_message, 
                   'store_list' : store_list,}

        return render(request, 'polls/results.html', context)

def vote(request):
    pass



def store_detail(request):

# 3안
    for index, row in to_df().iterrows():
        store = row['store']
        review = row['review']
        review_obj = Review(store=store, review=review)
        review_obj.save()

    store = request.GET.get('store')
    reviews = Review.objects.filter(store=store)
    reviews_list = [review.review for review in reviews]

    context = {'reviews': reviews_list}

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
