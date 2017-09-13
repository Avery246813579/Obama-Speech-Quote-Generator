from flask import Flask
app = Flask(__name__)

import Main

@app.route('/')
def hello_world():
    return 'Hello, World!<h1>Dogs</h1>' + Main.gram.random_word()
