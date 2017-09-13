from flask import Flask, request, jsonify, render_template, json
app = Flask(__name__)

import Main
import random
import os

generator = Main.Generator("test_data.txt")


@app.route('/new', methods=['POST'])
def new_tweet():
    body = json.loads(request.data)

    words = body['words']

    sentence = None
    if words is None:
        sentence = generator.generate_sentence(random.randint(0, 25))
    else:
        try:
            sentence = generator.generate_sentence(int(words))
        except TypeError:
            sentence = generator.generate_sentence(random.randint(0, 25))

    return jsonify({
        "success": True,
        "data": sentence
    })


@app.route('/')
def hello_world():
    words = request.args.get('words')

    sentence = None
    if words is None:
        sentence = generator.generate_sentence(random.randint(0, 25))
    else:
        try:
            sentence = generator.generate_sentence(int(words))
        except TypeError:
            sentence = generator.generate_sentence(random.randint(0, 25))

    return render_template('index.html', sentence=sentence)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

