from flask import Flask, render_template, jsonify, request
from query import *
import time


DAY = 86400


app = Flask(__name__)

@app.route('/_add_numbers')
def add_numbers():
    num_day = request.args.get('num_day')
    coin = request.args.get('coin')
    feature = request.args.get('feature')
    if num_day == "":
        num_day = 30
    current_time = time.time()

    start_time = int(current_time - int(num_day)*DAY)

    db = DB(assets=coin, time_begin=start_time, time_end=current_time, feature=feature)
    data = db.query()
    print(data)
    return jsonify(web_parse(data))

@app.route('/test')
def index():
    return render_template('main.html')
if __name__ == "__main__":
    app.run(debug=True)