from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


app.run('127.0.0.1', port=8000, debug=True)
