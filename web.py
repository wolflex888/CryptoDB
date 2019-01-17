from flask import Flask, render_template, jsonify, request
from query import *
import time


DAY = 86400


app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    num_day = request.args.get('num_day')
    # coin = request.args.get('bitcoin')+','+request.args.get('litecoin')+','+request.args.get('ethc')+','+request.args.get('eth')+','+request.args.get('bitcoinC')
    coin = request.args.get('coin')
    feature = request.args.get('feature')
    if num_day == "":
        num_day = 30
    current_time = time.time()
    # print(coin,"=====")
    start_time = int(current_time - int(num_day)*DAY)
    coin = coin.split(",")
    db = DB(assets=coin, time_begin=start_time, time_end=current_time, feature=feature)
    data = db.web_query()
    # print(web_parse(data, coin), coin)
    return jsonify(web_parse(data, coin))

@app.route('/test')
def index():
    return render_template('main.html')
if __name__ == "__main__":
    app.run(debug=True)