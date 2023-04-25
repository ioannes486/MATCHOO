from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.all()
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, "polls/results.html", context)

def vote(request, question_id):

    # <label for='activity'> 평소 활동적인걸 좋아하시나요 ? </label>
    # <input type='radio' id='activity' name='activity' value='yes' />좋아한다
    # <input type='radio' id='activity' name='activity' value='no' />좋아하지 않는다

    # # request['activity'] -> "yes" or "no"
    # if request['activity'] == 'yes':
    #     prompt += '나는 활동적인 것을 좋아해'
    # elif request['activity'] == 'no':
    #     prompt += '나는 활동적인 것을 좋아하지 않아'



    question = get_object_or_404(Question, pk=question_id)
    response = request.POST["choice"].split()
    primary_key = int(response[0])
    choice = response[1]

    try:
        selected_choice = question.choice_set.get(pk=primary_key)
    except (KeyError, Choice.DoesNotExist):
        context = {
            'question' : question,
            "error_message": "You didn't select a choice.",
        }
        return render(request, "polls/detail.html", context)
    else:
        selected_choice.votes +=1
        selected_choice.save()
        primary_key+=1
        context = {
            'primary_key' : primary_key,
        }
        #return redirect(f"polls/{primary_key}")wodjns
        return HttpResponse(reverse(f"polls:detail", args=(primary_key,)))

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
