from django.shortcuts import render
from django.views.decorators.http import require_POST

def index(request):
    context = {'title': 'Home'}
    return render(request, 'polls/index.html', context)

def detail(request):
    context = {'title': 'choice'}
    return render(request, 'polls/detail.html', context)

@require_POST
def results(request):
    result = list(request.POST.values())[1:]
    context = {'title': 'result and info', 'result': result}
    return render(request, 'polls/results.html', context)
