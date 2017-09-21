from flask import Flask, request, jsonify, render_template, json
import random
import os
import time

from MarkovModel import MarkovModel
import twitter
app = Flask(__name__)

model = MarkovModel("lib/static/test_data.txt", 3)
tweets = []

@app.route('/tweet', methods=['POST'])
def tweet():
    body = json.loads(request.data)

    # noinspection PyBroadException
    try:
        tweet_value = tweets[body['tweet']]
        twitter.tweet(tweet_value)

        return jsonify({
            "success": True
        })
    except Exception as e:
        return jsonify({
            "success": False
        })


@app.route('/new', methods=['POST'])
def new_tweet():
    body = json.loads(request.data)

    words = body['words']

    sentence = None
    if words is None:
        sentence = model.generate_sentence(random.randint(10, 25))
    else:
        try:
            sentence = model.generate_sentence(int(words))
        except ValueError:
            sentence = model.generate_sentence(random.randint(10, 25))

    tweets.append(sentence)
    return jsonify({
        "success": True,
        "data": sentence,
        "id": len(tweets) - 1
    })


@app.route('/')
def hello_world():
    words = request.args.get('words')

    sentence = None
    if words is None:
        sentence = model.generate_sentence(random.randint(10, 25))
    else:
        try:
            sentence = model.generate_sentence(int(words))
        except TypeError:
            sentence = model.generate_sentence(random.randint(10, 25))

    tweets.append(sentence)
    return render_template('index.html', sentence=sentence, id="**/" + str(len(tweets) - 1) + "/**", time=time.time(),
                           words=model.map_gram.word_count, lines=model.map_gram.line_count)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

