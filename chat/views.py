# Note: you need to be using OpenAI Python v0.27.0 for the code below to work

import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import openai

openai.api_key = 'myapi'

def home(request):
    return render(request, 'chat/home.html')



@csrf_exempt
def generate_text(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
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
        return JsonResponse({'messages': messages})



