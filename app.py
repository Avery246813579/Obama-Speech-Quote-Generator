import os

import psycopg2
from flask import Flask, request, jsonify, send_from_directory, json
from lib.twitter import tweet
from RainbowChain import RainbowChain

app = Flask(__name__)

conn = psycopg2.connect("dbname=dds7q3a5dl5c45 user=edksigbbpxnyrh password=" +
                        os.environ.get('DATABASE_PASSWORD') + " host=" + os.environ.get('DATABASE_HOST'))

tweets = []

print("ONE")
model = RainbowChain('static/data/raw_corpus.txt', 3)
print("TWO")

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
        tweet(tweet_value)

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
def get_favorite_tweets():
    return jsonify({
        "success": True,
        "data": favorites
    })


@app.route('/new', methods=['POST'])
def generate_new_tweet():
    sentence = model.generate_sentence()
    tweets.append(sentence)

    return jsonify({
        "success": True,
        "data": sentence,
        "id": len(tweets) - 1
    })


@app.route('/')
def default_route():
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
    return send_from_directory('react-website/build', 'index.html')


print("HERE3")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
    print("HERE5")

print("HERE4")
