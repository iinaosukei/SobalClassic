from flask import Flask, request, session
import requests
import json

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = 'your_secret_key'

GET_THEME_PROMPT = 'Think of an appropriate situation.Be sure to return it in json format.situation:str The content of str is in Japanese.'
# CHATGPT_API_KEY = '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'
CHATGPT_API_KEY = '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'

@app.route('/')
def index():
    # 合計得点の初期値を設定
    session['totalPoints'] = 0

    return app.send_static_file('front/index.html')

@app.route('/result')
def ranking():
    return app.send_static_file('front/result.html')

@app.route('/battle')
def battle():
    return app.send_static_file('front/battle.html')

@app.route('/get_chatgpt_response/<character>', methods=['POST'])
def get_chatgpt_response(character):
    # 呼ぶと採点される
    # 形式：'question': text

    print(character)
    user_question = request.json['question']
    chatgpt_response = _generate_chatgpt_response(user_question, character)
    return json.dumps(chatgpt_response)

def _get_tamura_text(file_path):
    # ファイルを読み込みモードで開く
    with open(file_path, 'r', encoding='utf-8') as file:
        # ファイルの中身を文字列として取得
        file_content = file.read()
    return file_content

def _generate_chatgpt_response(user_question, character):
    # ここのif文内で好きな人格に変更する
    # character_promptは仮の変数
    if character == 'T1':
        file_path = 'tamura.txt'
    elif character == 'T2':
        file_path = 'takazawa.txt'
    else:
        file_path = 'furumoto.txt'

    prompt = (f'Score the following compliments on a 10-point scale, indicating the score only. The rating is dry.「{user_question}」Be sure to use the json format, and be sure to display only the following:point:int, detailed_evaluation_criteria:str. detailed_evaluation_criteria is in Japanese.')
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Authorization': 'Bearer ' + CHATGPT_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{
                        'role': 'system',
                        'content': _get_tamura_text(file_path)
                     },
                     {
                        'role': 'user',
                        'content': prompt
                     }],
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    response_json = response.json()
    content = response_json['choices'][0]['message']['content']
    print(content)
    print(type(content))
    content_json = json.loads(content)
    print (content_json['point'])
    print (content_json['detailed_evaluation_criteria'])

    # 合計点数を記録
    session['totalPoints'] += content_json['point']
    content_json['total_points'] = session['totalPoints']
    response_json['choices'][0]['message']['content'] = json.dumps(content_json)

    return response_json['choices'][0]['message']['content'].strip()

app.run(port=8000, debug=True)