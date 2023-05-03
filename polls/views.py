from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.urls import reverse
from django.views import generic
import json
import openai
from ._crawling import crawl_reviews, to_df
from ._chat import recommand_traveling_site
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
        bot_message = recommand_traveling_site(res)
        bot_message = '강남맛집'
        crawl_reviews(bot_message)
        store_list = to_df().store.tolist()
        reviews_list = to_df().review.tolist()
        prediction_list = to_df().prediction.tolist()

        context = {
            'bot_message': bot_message, 
            'store_list' : store_list,
            'reviews_list' : reviews_list,
            'prediction_list' : prediction_list
                   }

    
        return render(request, 'polls/results.html', context)

def vote(request):
    pass

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
