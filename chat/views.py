import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import FileUploadForm
import openai

openai.api_key = 'mine'


def home(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            # 파일 내용을 검색어로 사용합니다.
            content = file.read().decode('utf-8')
            response = requests.get(f'https://api.openai.com/v1/search?model=davinci&query={content}&documents=3')
            results = response.json()['data']
            # 검색 결과를 출력합니다.
            messages = [{'role': 'assistant', 'text': result['text']} for result in results]
            return JsonResponse({'messages': messages})
    else:
        form = FileUploadForm()
    return render(request, 'chat/home.html', {'form': form})


@csrf_exempt
def generate_text(request):
    if request.method == 'POST':
        messages = []
        # sample.txt 파일 경로를 입력합니다.
        file_path = 'C:/Users/TECH2_25/Desktop/MATCHOO/sample.txt'
        with open(file_path, 'rt', encoding='utf-8') as f:
            # 파일의 모든 내용을 읽어옵니다.
            content = f.read()
            # 파일 내용을 검색어로 사용합니다.
            response = requests.get(f'https://api.openai.com/v1/search?model=davinci&query={content}&documents=1')
            results = response.json().get('data', [])
            # 검색 결과가 있을 때 메시지에 추가합니다.
            if results:
                for result in results:
                    messages.append({'role': 'assistant', 'text': result['text']})
            # 검색 결과가 없을 때 에러 메시지를 추가합니다.
            else:
                messages.append({'role': 'assistant', 'text': '검색 결과를 찾을 수 없습니다.'})
        return JsonResponse({'messages': messages})

