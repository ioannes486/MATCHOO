import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import openai

openai.api_key = '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'

def home(request):
    return render(request, 'chat/home.html')


@csrf_exempt
def generate_text(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        messages = [{'role': 'user', 'text': user_message}]
        completion = openai.Completion.create(
            engine='text-davinci-003',
            prompt='\n'.join([f'{m["role"]}: {m["text"]}' for m in messages]),
            temperature=0.5,
            max_tokens=1024,
            n=1,
            stop=None,
            timeout=15,
        )
        assistant_message = completion.choices[0].text.strip()
        messages.append({'role': 'assistant', 'text': assistant_message})
        return JsonResponse({'messages': messages})

# 설문조사바탕으로 답변된 항목을 텍스트로 바꿔서 
# 답변이 ai에 들어가서 자동 리다이렉트