import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def home(request):
    return render(request, 'chat/home.html')

@csrf_exempt
def generate_text(request):
    input_text = request.POST.get('input_text', '')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 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',
    }
    data = {
        'prompt': input_text,
        'max_tokens': 50,
    }
    response = requests.post('https://api.openai.com/v1/engines/davinci-codex/completions', headers=headers, json=data)
    output_text = response.json().get('completions', [{}])[0].get('text', '응답없음')
    return JsonResponse({'output_text': output_text})

