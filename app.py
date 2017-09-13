from flask import Flask
app = Flask(__name__)

import Main
import os

@app.route('/')
def hello_world():
    return 'Hello, World!<h1>Dogs</h1>' + Main.gram.random_word()

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
