from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

GET_THEME_PROMPT = 'Think of an appropriate situation.Be sure to return it in json format.situation:str The content of str is in Japanese.'
CHATGPT_API_KEY = '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'

@app.route('/get_theme', methods=['GET'])
def get_theme():
    # 呼ぶとテーマが返る
    print('theme')


@app.route('/get_chatgpt_response', methods=['POST'])
def get_chatgpt_response():
    # 呼ぶと採点される
    # 形式：'question': text
    user_question = request.json['question']
    chatgpt_response = _generate_chatgpt_response(user_question)
    return json.dumps(chatgpt_response)


def _generate_chatgpt_response(user_question):
    prompt = (f'Score the following compliments on a 100-point scale, indicating the score only. The rating is dry.「{user_question}」Be sure to use the json format, and be sure to display only the following:point:int, detailed_evaluation_criteria:str')
    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Authorization': 'Bearer ' + CHATGPT_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 50
    }
    response = requests.post(url, json=data, headers=headers)
    response_json = response.json()
    content = response_json['choices'][0]['message']['content']
    print(content)
    print(type(content))
    content_json = json.loads(content)
    print (content_json['point'])
    print (content_json['detailed_evaluation_criteria'])
    return response_json['choices'][0]['message']['content'].strip()


if __name__ == '__main__':
    app.run(debug=True)
