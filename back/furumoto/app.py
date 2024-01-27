import json
import re
from flask import  request

data = {"name": "Alice", "score": 80},{"name": "Bob", "score": 90},{"name": "Charlie", "score": 75},{"name": "David", "score": 95},{"name": "Eve", "score": 85}

# フォームから名前を取得
user = request.form['name']

# JSON形式の文章から数字のみを抽出する関数
def extract_numbers(json_text):
    numbers = []
    # 正規表現を使って数字のみを抽出
    pattern = r'\b\d+\b'
    matches = re.findall(pattern, json_text)
    for match in matches:
        numbers.append(int(match))
    return numbers

# JSON形式の文章から数字のみを抽出
numbers = extract_numbers()

# JSONデータをPythonオブジェクトにパース
data[user] = numbers

# スコアで降順にソート
data.sort(key=lambda x: x['score'], reverse=True)

# ランキング用のリストに格納
ranking = [(entry['name'], entry['score']) for entry in data]

