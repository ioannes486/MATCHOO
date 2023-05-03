import openai
from ._crawling import crawl_reviews, to_df
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def recommand_traveling_site(res):
    # 요청 받아서 문구 만들기
    user_message = '앞으로 단답으로만 대답해 나는 {}고 {}고 {}고 {}고 {}고 {}해 나한테 부연설명,부가설명없이 단답형으로 한국 여행지 한 곳 무조건 이름만 추가설명없이 나오게 해줘'.format(res.get('trip'), res.get('type'), res.get('movement'), res.get('pop'), res.get('with'), res.get('how'), )

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
    #bot_message = '강남맛집'

    return bot_message