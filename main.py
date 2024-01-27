from flask import Flask
app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('front/index.html')

@app.route('/ranking')
def ranking():
    return app.send_static_file('front/ranking.html')

@app.route('/battle')
def battle():
    return app.send_static_file('front/battle.html')

app.run(port=8000, debug=True)