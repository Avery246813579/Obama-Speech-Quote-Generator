from flask import Flask, request, jsonify, render_template, json
app = Flask(__name__)

import random
import os
import time
import MapGram
import twitter

model = MapGram.MarkovModel("test_data.txt")

@app.route('/new', methods=['POST'])
def tweet():
    body = json.loads(request.data)

    twitter.tweet(body['tweet'])

    return jsonify({
        "success": True
    })


@app.route('/tweet', methods=['POST'])
def new_tweet():
    body = json.loads(request.data)

    words = body['words']

    sentence = None
    if words is None:
        sentence = model.generate_sentence(random.randint(0, 25))
    else:
        try:
            sentence = model.generate_sentence(int(words))
        except ValueError:
            sentence = model.generate_sentence(random.randint(0, 25))

    return jsonify({
        "success": True,
        "data": sentence
    })


@app.route('/')
def hello_world():
    words = request.args.get('words')

    sentence = None
    if words is None:
        sentence = model.generate_sentence(random.randint(0, 25))
    else:
        try:
            sentence = model.generate_sentence(int(words))
        except TypeError:
            sentence = model.generate_sentence(random.randint(0, 25))

    return render_template('index.html', sentence=sentence, time=time.time())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

