from flask import Flask, render_template, request
from crossover import Crossover

switcher = Crossover()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def button():
    print(request.json)

    request_data = request.get_json()

    switcher_code = request_data['button']
    switcher_mode = request_data['mode']

    switcher.remote_switch(switcher_code, "cut")


    return "0"