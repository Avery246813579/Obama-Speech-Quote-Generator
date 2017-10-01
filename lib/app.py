import os
import time

import psycopg2
from flask import Flask, request, jsonify, render_template, json

import twitter
from MarkovModel import MarkovModel

app = Flask(__name__)

conn = psycopg2.connect("dbname=dds7q3a5dl5c45 user=edksigbbpxnyrh password=" +
                        os.environ.get('DATABASE_PASSWORD') + " host=" + os.environ.get('DATABASE_HOST'))

model = MarkovModel("lib/static/test_data.txt", 3)
tweets = []

cur = conn.cursor()

cur.execute("SELECT * FROM Tweets;")
favorites_raw = list(cur.fetchall())
favorites = []

for i in range(len(favorites_raw)):
    favorites.append(favorites_raw[i][1])

cur.close()

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


# TODO: Check if tweet was already tweeted

@app.route('/favorite_tweet', methods=['POST'])
def favorite_tweet():
    body = json.loads(request.data)

    # noinspection PyBroadException
    try:
        tweet_value = tweets[body['tweet']]
        cur = conn.cursor()

        cur.execute("SELECT * FROM Tweets WHERE content='%s';" % (tweet_value))

        if len(cur.fetchall()) > 0:
            return jsonify({
                "success": False,
                "message": "Already exists"
            })

        favorites.append(tweet_value)
        cur.execute("INSERT INTO Tweets (content) VALUES (%s);" % ("'" + tweet_value + "'"))

        conn.commit()
        cur.close()

        return jsonify({
            "success": True,
            "data": tweet_value
        })
    except Exception as e:
        print(e)
        return jsonify({
            "success": False,
            "message": "Can't pasrse"
        })




@app.route('/favorite_tweets', methods=['GET'])
def favorite_tweets():
    return jsonify({
        "success": True,
        "data": favorites
    })


@app.route('/new', methods=['POST'])
def new_tweet():
    body = json.loads(request.data)

    words = body['words']

    sentence = None
    if words is None:
        sentence = model.generate_sentence()
    else:
        try:
            sentence = model.generate_sentence()
        except ValueError:
            sentence = model.generate_sentence()

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
        sentence = model.generate_sentence()
    else:
        try:
            sentence = model.generate_sentence()
        except TypeError:
            sentence = model.generate_sentence()

    tweets.append(sentence)
    print(favorites)
    return render_template('index.html', sentence=sentence, id="**/id =" + str(len(tweets) - 1) + "/**", time=time.time(),
                           words=model.dictogram.word_count, lines=model.dictogram.line_count)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

